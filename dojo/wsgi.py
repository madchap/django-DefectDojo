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
from socket import error as socket_error
import logging

logger = logging.getLogger(__name__)

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "dojo.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dojo.settings.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application

# opentelemetry
from uwsgidecorators import postfork
from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor
)


@postfork
def init_tracing():
    if os.environ.get('DD_ENABLE_TELEMETRY') in ('true', 'True'):
        logger.info("Anonymous telemetry is enabled. See <LINK> for more information.")
        resource = Resource.create(attributes={
            "defectdojo": "uwsgi"
        })

        trace.set_tracer_provider(TracerProvider(resource=resource))
        #  span_processor = BatchSpanProcessor(
        #    OTLPSpanExporter(endpoint="http://191.168.10.68:4317")
        # )
        span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
        trace.get_tracer_provider().add_span_processor(span_processor)
    else:
        logger.info("Telemetry is disabled per DD_ENABLE_TELEMETRY variable.")


application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)


def _check_ptvsd_port_not_in_use(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', port))
    except socket_error as se:
        return False

    return True


ptvsd_port = 3000
if os.environ.get("DD_DEBUG") == "True" and _check_ptvsd_port_not_in_use(ptvsd_port):
    try:
        # enable remote debugging
        import ptvsd
        ptvsd.enable_attach(address=('0.0.0.0', ptvsd_port))
        print("ptvsd listening on port " + ptvsd_port)
    except Exception as e:
        print("Generic exception caught with DD_DEBUG on. Passing.")
