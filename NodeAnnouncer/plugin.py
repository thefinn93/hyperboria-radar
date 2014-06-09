###
# Copyright (c) 2012, Finn Herzfeld
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

# import supybot.utils as utils
from supybot.commands import *
# import supybot.plugins as plugins
# import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
# import time
import supybot.ircmsgs as ircmsgs
import supybot.schedule as schedule
import json

_ = PluginInternationalization('NodeAnnouncer')

@internationalizeDocstring
class NodeAnnouncer(callbacks.Plugin):
    """Checks the JSON file every minute
    and announced new nodes in the specified channels"""

    def __init__(self, irc):
        self.__parent = super(NodeAnnouncer, self)
        self.__parent.__init__(irc)
        self.debug = False
        try:
            schedule.removeEvent('hyperboriaNodeChecker')
        except KeyError:
            pass

        def checkForNodes():
            self.checkNodes(irc)
        try:
            schedule.addPeriodicEvent(checkForNodes, 5, 'hyperboriaNodeChecker', False)
        except AssertionError:
            irc.queueMsg(ircmsgs.privmsg("#bollocks", 'Error: the node checker was already running!'))
        else:
            irc.queueMsg(ircmsgs.privmsg("#bollocks",'Node checker started!'))

        self.irc = irc

    def checkNodes(self, irc):
        if(self.debug):
            irc.queueMsg(ircmsgs.privmsg("#bollocks", "Checking for new nodes"))
        try:
            unannounced = json.load(open("/tmp/unannounced_nodes.json"))
            for node in unannounced:
                irc.queueMsg(ircmsgs.privmsg("#radar","New node spotted: " + str(node)))
            jsonfile = open("/tmp/unannounced_nodes.json", "w+")
            jsonfile.write("[]")
            jsonfile.close()
        except Exception as inst:
            irc.queueMsg(ircmsgs.privmsg("#bollocks", "ERROR: " + str(inst)))

    def start(self, irc, msg, args):
        """takes no arguments

        A command to start the node checker."""
        # don't forget to redefine the event wrapper
        def checkForNodes():
            self.checkNodes(irc)
        try:
            schedule.addPeriodicEvent(checkForNodes, 5, 'hyperboriaNodeChecker', False)
        except AssertionError:
            irc.reply('Error: the node checker was already running!')
        else:
            irc.reply('Node checker started!')
    start = wrap(start)

    def debugMode(self, irc, msg, args):
        """takes no arguments

        toggles debug mode either on or off"""
        if(self.debug):
            self.debug = False
            irc.reply("Debug mode disabled")
        else:
            self.debug = True
            irc.reply("Debug mode enabled")

    debugMode = wrap(debugMode)

    def stop(self, irc, msg, args):
        """takes no arguments

        A command to stop the node checker."""
        try:
            schedule.removeEvent('hyperboriaNodeChecker')
        except KeyError:
            irc.reply('Error: the node checker wasn\'t running!')
        else:
            irc.reply('Node checker stopped.')
    stop = wrap(stop)

Class = NodeAnnouncer
