#! /usr/bin/env python
import ConfigParser
import sys
import json
import time
import subprocess
import socket
import requests
import urllib
import tweepy

sys.path.append("/opt/cjdns/contrib/python/")

nodefile = "/home/finn/supybot/data/known_nodes.json"

twitter_name = "thefinn93"

auth = tweepy.OAuthHandler("xxx", "xxx")
auth.set_access_token("xxx", "xxx")
api = tweepy.API(auth)

socialnodeauth=("nodebot","xxx")

from cjdnsadmin import connectWithAdminInfo
try:
    cjdns = connectWithAdminInfo()
except Exception as e:
    # requests.get("https://www.thefinn93.com/push/send?" + urllib.urlencode({"token":"ExT2G6xP9RlireefbIIt","title":"NodeCheck.py on Mal", "message": str(e)}))
    sys.exit(1)

try:
    knownnodes = json.load(open(nodefile))
except:
    sys.exit()

more = True
i = 0

count = 0
for lastseen in knownnodes:
    if knownnodes[lastseen] > time.time()-604800:
        count += 1

#print  str(count) + " nodes seen this week"
try:
	announceme = json.load(open("/tmp/unannounced_nodes.json"))
except:
	announceme = []

while more:
    dump = cjdns.NodeStore_dumpTable(i)
    more = "more" in dump
    for node in dump["routingTable"]:
        if not node['ip'] in knownnodes:
            announceme.append(node['ip'])
            count += 1
            newstatus = "New Hyperboria Node detected! Welcome, %s!" %node['ip']
            requests.post("http://socialno.de/api/statuses/update.json", data={"status": newstatus}, auth=socialnodeauth)
            api.update_status(newstatus)
#            t.direct_message.new(user="thefinn93", text="I works")
        knownnodes[node['ip']] = time.time()
    i = i + 1

json.dump(knownnodes, open(nodefile, "w"), sort_keys=True, indent=4)
json.dump(announceme, open("/tmp/unannounced_nodes.json", "w"), sort_keys=True, indent=4)
