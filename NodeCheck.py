#! /usr/bin/env python
import sys
import json
import time
import requests
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
    print("Failed to import cjdns")
    sys.exit(1)

try:
    knownnodes = json.load(open(nodefile))
except IOError, ValueError:
    sys.exit()

more = True
i = 0

count = 0
for lastseen in knownnodes:
    if knownnodes[lastseen] > time.time()-604800:
        count += 1

try:
	announceme = json.load(open("/tmp/unannounced_nodes.json"))
except IOError, ValueError:
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
