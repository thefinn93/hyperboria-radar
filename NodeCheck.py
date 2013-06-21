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

auth = tweepy.OAuthHandler("xxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxx")
auth.set_access_token("xxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxx")
api = tweepy.API(auth)


from cjdnsadmin import connectWithAdminInfo
try:
    cjdns = connectWithAdminInfo()
except:
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
            api.update_status("New Hyperboria Node detected! Welcome, %s!" % node['ip'])
#            t.direct_message.new(user="thefinn93", text="I works")
        knownnodes[node['ip']] = time.time()
    i = i + 1

json.dump(knownnodes, open(nodefile, "w"), sort_keys=True, indent=4)
json.dump(announceme, open("/tmp/unannounced_nodes.json", "w"), sort_keys=True, indent=4)
