import httplib
import urllib
import json
from urlparse import urlparse

class AlertaClient:
    
    def __init__(self, host, key, env='Production'):
    	self.env = env
    	self.up = urlparse(host)
	self.host = self.up.netloc
	if self.up.path[-1:] != '/':
	    self.path = self.up.path + '/'
	else:
	    self.path = self.up.path
    	self.header = {"Content-Type": "application/json", "Authorization": "Key " + key}

    def heartbeat(self, origin, timeout=3600, tags=[]):
	self.uri = self.path+"/heartbeat"
	self.body = { "origin": origin, "timeout": timeout, "tags":tags}

    # service - where it happend
    # resource - with what it happend
    # event - what happend, in short
    # value - value of happens, if applicable
    # text - what exactly happened, in detail
    def alert(self, service, resource, event, value, text, environment=None, rawData=None, severity='major', correlate=[], status='open', group='Misc', tags=[], attributes={}, origin=None, type=None, timeout=86400):
	environment = environment if environment is not None else self.env
	self.uri = self.path+"/alert"
	self.body = {
	    "service": service,
	    "resource": resource,
	    "event": event,
	    "value": value,
	    "text": text,
	    "environment": environment,
	    "rawData": rawData,
	    "severity": severity,
	    "correlate": correlate,
	    "status": status,
	    "group": group,
	    "tags": tags,
	    "attributes": attributes, 
	    "origin": origin, 
	    "type": type,
	    "timeout": timeout}

    def send(self):
	print self.host
	conn = httplib.HTTPConnection(self.host)
	conn.request('POST', self.uri, json.dumps(self.body), self.header)
	response = conn.getresponse()
	if response.status != 201:
	    return response.status
	else:
	    return None
