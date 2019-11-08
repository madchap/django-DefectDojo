import json
import hashlib
from urllib.parse import urlparse
from dojo.models import Endpoint, Finding

__author__ = 'Kirill Gotsman'


class HackerOneJSONParser(object):

    def __init__(self, file, test):
        self.dupes = dict()
        self.items = ()
        if file is None:
            return
        data = file.read()
        try:
            tree = json.loads(str(data, 'utf-8'))
        except:
            tree = json.loads(data)
        for content in tree["data"]:
            try:
                title = content["attributes"]["title"]
            except:
                pass
            description = content["attributes"]["vulnerability_information"]
            try:
                severity = content["relationships"]["severity"]["data"]["attributes"]["rating"].capitalize()
                if severity not in ["Low", "Medium", "Hight", "Critical"]:
                    severity = "Info" 
            except:
                severity = "Info"           
            cwe = content["relationships"]["weakness"]["data"]["attributes"]["external_id"]
            
            try:
                references = ("[https://hackerone.com/reports/"+content["id"] + "](http://)" + 
                "\n" + "[https://cloudbees.atlassian.net/browse/" + content["attributes"]["issue_tracker_reference_id"] + "](http://)")
            except:
                references = ("[https://hackerone.com/reports/" + content["id"] + "](http://)")

            if content["attributes"]["state"] in ["triaged","new"]:
                active=True
            else:
                active=False
            
            try:
                cwe = int(content["relationships"]["weakness"]["data"]["attributes"]["external_id"][4:])
            except:
                cwe = 0

            dupe_key = hashlib.md5(str(references + title).encode('utf-8')).hexdigest()
            if dupe_key in self.dupes:
                finding = self.dupes[dupe_key]
                if finding.references:
                    finding.references = finding.references
                self.dupes[dupe_key] = finding
            else:
                self.dupes[dupe_key] = True

                finding = Finding(
                    title=title,
                    test=test,
                    active=True,
                    verified=False,
                    description=description,
                    severity=severity,
                    numerical_severity=Finding.get_numerical_severity(severity),
                    mitigation="See description",
                    impact="No impact provided",
                    references=references,
                    cwe=cwe,
                    dynamic_finding=True,)
                finding.unsaved_endpoints = list()
                self.dupes[dupe_key] = finding
            self.items = self.dupes.values()
