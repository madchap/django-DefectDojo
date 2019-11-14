import json
import hashlib
from urllib.parse import urlparse
from dojo.models import Endpoint, Finding

__author__ = 'Kirill Gotsman'


class HackerOneJSONParser(object):
    """
    A class that can be used to parse the Get All Reports JSON export from HackerOne API.
    A typical Get All Reports JSON export looks like the following:

    {
    "data": [{
      "id": "1337",
      "type": "report",
      "attributes": {
        "title": "XSS in login form",
        "state": "new",
        "created_at": "2016-02-02T04:05:06.000Z",
        "vulnerability_information": "...",
        "triaged_at": null,
        "closed_at": null,
        "last_reporter_activity_at": null,
        "first_program_activity_at": null,
        "last_program_activity_at": null,
        "bounty_awarded_at": null,
        "last_activity_at": null,
        "last_public_activity_at": null,
        "swag_awarded_at": null,
        "disclosed_at": null,
        "source": null,
        "reporter_agreed_on_going_public_at": null
      },
      "relationships": {
        "reporter": {
          "data": {
            "id": "1337",
            "type": "user",
            "attributes": {
              "username": "api-example",
              "name": "API Example",
              "disabled": false,
              "created_at": "2016-02-02T04:05:06.000Z",
              "profile_picture": {
                "62x62": "/assets/avatars/default.png",
                "82x82": "/assets/avatars/default.png",
                "110x110": "/assets/avatars/default.png",
                "260x260": "/assets/avatars/default.png"
              }}}},
        "assignee": {
          "data": {
            "id": "1337",
            "type": "user",
            "attributes": {
              "username": "member",
              "name": "Member",
              "disabled": false,
              "created_at": "2016-02-02T04:05:06.000Z",
              "profile_picture": {
                "62x62": "/assets/avatars/default.png",
                "82x82": "/assets/avatars/default.png",
                "110x110": "/assets/avatars/default.png",
                "260x260": "/assets/avatars/default.png"
              }}}},
        "program": {
          "data": {
            "id": "1337",
            "type": "program",
            "attributes": {
              "handle": "security",
              "created_at": "2016-02-02T04:05:06.000Z",
              "updated_at": "2016-02-02T04:05:06.000Z"
            }}},
        "severity": {
          "data": {
            "id": "57",
            "type": "severity",
            "attributes": {
              "rating": "high",
              "author_type": "User",
              "user_id": 1337,
              "created_at": "2016-02-02T04:05:06.000Z",
              "score": 8.7,
              "attack_complexity": "low",
              "attack_vector": "adjacent",
              "availability": "high",
              "confidentiality": "low",
              "integrity": "high",
              "privileges_required": "low",
              "user_interaction": "required",
              "scope": "changed"
            }}},
        "weakness": {
          "data": {
            "id": "1337",
            "type": "weakness",
            "attributes": {
              "name": "Cross-Site Request Forgery (CSRF)",
              "description": "The web application does not, or can not, sufficiently verify whether a well-formed, valid, consistent request was intentionally provided by the user who submitted the request.",
              "external_id": "cwe-352",
              "created_at": "2016-02-02T04:05:06.000Z"
            }}},
        "structured_scope": {
          "data": {
            "id": "57",
            "type": "structured-scope",
            "attributes": {
              "asset_identifier": "api.example.com",
              "asset_type": "url",
              "confidentiality_requirement": "high",
              "integrity_requirement": "high",
              "availability_requirement": "high",
              "max_severity": "critical",
              "created_at": "2015-02-02T04:05:06.000Z",
              "updated_at": "2016-05-02T04:05:06.000Z",
              "instruction": null,
              "eligible_for_bounty": true,
              "eligible_for_submission": true,
              "reference": "H001001"
            }} },
        "bounties": {
          "data": []},
        "custom_field_values": {
          "data": []
        }A}},
    "..."
  ],
  "links": {
    "self": "https://api.hackerone.com/v1/reports?filter%5Bprogram%5D%5B%5D=security&page%5Bnumber%5D=1",
    "next": "https://api.hackerone.com/v1/reports?filter%5Bprogram%5D%5B%5D=security&page%5Bnumber%5D=2",
    "last": "https://api.hackerone.com/v1/reports?filter%5Bprogram%5D%5B%5D=security&page%5Bnumber%5D=5"
  }
}
    """

    def __init__(self, file, test):
        """
        Converts a HackerOne reports to a DefectDojo finding
        """
        self.dupes = dict()
        # Start with an empty findings
        self.items = ()
        # Exit if file is not provided
        if file is None:
            return
        # Load the contents of the JSON file into a dictionary
        data = file.read()
        try:
            tree = json.loads(str(data, 'utf-8'))
        except:
            tree = json.loads(data)
        # Conver JSON  report to DefectDojo format
        for content in tree["data"]:
            # Build the title of the Dojo finding
            try:
                title = content["attributes"]["title"]
            except:
                pass
            # Build the description of the Dojo finding
            description = content["attributes"]["vulnerability_information"]
            # Build the severity of the Dojo finding
            try:
                severity = content["relationships"]["severity"]["data"]["attributes"]["rating"].capitalize()
                if severity not in ["Low", "Medium", "Hight", "Critical"]:
                    severity = "Info" 
            except:
                severity = "Info"
            # Build the references of the Dojo finding         
            try:
                references = ("[https://hackerone.com/reports/"+content["id"] + "](http://)" + 
                "\n" + "[https://cloudbees.atlassian.net/browse/" + content["attributes"]["issue_tracker_reference_id"] + "](http://)")
            except:
                references = ("[https://hackerone.com/reports/" + content["id"] + "](http://)")
            # Set active state of the Dojo finding 
            if content["attributes"]["state"] in ["triaged","new"]:
                active=True
            else:
                active=False
            # Set CWE of the Dojo finding 
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

                # Build and return Finding model
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
