"""
WSGI config for dojo project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import socket
import logging
import uuid
from django.conf import settings
from dojo import __version__

logger = logging.getLogger(__name__)

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "dojo.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dojo.settings.settings")


# opentelemetry
from uwsgidecorators import postfork
from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    BatchSpanProcessor
)


@postfork
def init_tracing():
    if os.environ.get('DD_ENABLE_TELEMETRY') in ('true', 'True'):
        logger.info("Anonymous telemetry is enabled per DD_ENABLE_TELEMETRY variable. See <LINK> for more information.")
        # create a JaegerExporter
        # can launch a quick one like
        # docker run -d -p 5775:5775/udp -p 6831:6831/udp -p 16686:16686 jaegertracing/all-in-one:latest
        jaeger_exporter = JaegerExporter(
            # configure agent
            agent_host_name='192.168.10.68',
            agent_port=6831,
            # optional: configure also collector
            # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
            # username=xxxx, # optional
            # password=xxxx, # optional
            # max_tag_value_length=None # optional
        )
        # TODO: Store in DB
        instance_id = uuid.uuid5(uuid.NAMESPACE_DNS, settings.SITE_URL)
        logger.info(f"Service instance ID is {instance_id}")
        resource = Resource.create(attributes={
            "service.name": "DefectDojo",
            "service.instance.id": f"{instance_id}",
            "service.version": __version__
        })

        trace.set_tracer_provider(TracerProvider(resource=resource))
        span_jaeger_processor = BatchSpanProcessor(jaeger_exporter)
        span_console_processor = SimpleSpanProcessor(ConsoleSpanExporter())
        trace.get_tracer_provider().add_span_processor(span_jaeger_processor)
        trace.get_tracer_provider().add_span_processor(span_console_processor)
    else:
        logger.info("Telemetry is disabled per DD_ENABLE_TELEMETRY variable.")


# Shouldn't apply to docker-compose dev mode (1 process, 1 thread), but may be needed when enabling debugging in other contexts
def is_debugger_listening(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s.connect_ex(('127.0.0.1', port))


debugpy_port = os.environ.get("DD_DEBUG_PORT") if os.environ.get("DD_DEBUG_PORT") else 3000

# Checking for RUN_MAIN for those that want to run the app locally with the python interpreter instead of uwsgi
if os.environ.get("DD_DEBUG") == "True" and not os.getenv("RUN_MAIN") and is_debugger_listening(debugpy_port) != 0:
    print("DD_DEBUG is set to True, setting remote debugging on port {}".format(debugpy_port))
    import traceback
    try:
        import debugpy

        # Required, otherwise debugpy will try to use the uwsgi binary as the python interpreter - https://github.com/microsoft/debugpy/issues/262
        debugpy.configure({
                            "python": "python",
                            "subProcess": True
                        })
        debugpy.listen(("0.0.0.0", debugpy_port))
        print("DebugPy listening on port {}".format(debugpy_port))
        if os.environ.get("DD_DEBUG_WAIT_FOR_CLIENT") == "True":
            print("Waiting for the debugging client to connect on port {}".format(debugpy_port))
            debugpy.wait_for_client()
            print("Debugging client connected, resuming execution")
    except Exception as e:
        print("Exception caught while enabling debug mode, passing. \nPrinting error {}".format(traceback.format_exc()))
        pass

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
