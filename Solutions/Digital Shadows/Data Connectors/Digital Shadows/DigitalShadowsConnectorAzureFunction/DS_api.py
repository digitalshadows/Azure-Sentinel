""" handles all DS api related functions """
import logging
import requests
import base64
from urllib.parse import urlparse

logger = logging.getLogger("DS_api")

class api:

    def __init__(self, id, key, secret, url):
        """ 
            constructer initializes the DS creds and creates passkey.
            Parses the url recieved from user.
        """
        u = urlparse(url)

        self.url = "https://" + u.netloc + u.path + "/"
        passkey = key + ":" + secret
        self.id = id
        self.b64val = base64.b64encode(bytes(passkey, 'utf-8')).decode("ascii")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": "Basic %s" % self.b64val,
            "searchlight-account-id": "%s" % self.id,
            "User-Agent": "DigitalShadowsAzureSentinelIntegration"
        })

    def get_alerts(self, alert_ids):
        """ 
            function for getting alerts using id
        """

        alert_url = self.url + "alerts"
        params = dict(id=alert_ids)
        response = self.session.get(alert_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_incidents(self, incident_ids):
        """ 
            function for getting incidents using id list
        """
        incident_url = self.url + "incidents"
        params = dict(id=incident_ids)
        response = self.session.get(incident_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_triage_events(self, before_date, after_date):
        """ 
            function for getting triage events,
            send only the DS converted dates using state serializer functions to get triage events
        """
        params = {"limit": 20, "event-created-before": str(before_date), "event-created-after": str(after_date)}
        triage_url = self.url + "triage-item-events"
        response = self.session.get(triage_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_triage_items(self, triage_ids):
        """  
            gets triage items from the triage events
        """

        items_url = self.url + "triage-items"
        params = dict(id=triage_ids)
        params['limit'] = 1000
        response = self.session.get(items_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_triage_comments(self, item_id):
        """  
            gets triage comments from the triage items
        """

        items_url = self.url + "triage-items/" + str(item_id) + "/comments"
        response = self.session.get(items_url)
        response.raise_for_status()
        return response.json()
    
    def get_triage_events_by_num(self, event):
        """
            gets triage events by number
        """
        params = {"limit": 20, "event-num-after": str(event)}
        triage_url = self.url + "triage-item-events" 
        response = self.session.get(triage_url, params=params)
        response.raise_for_status()
        return response.json()
