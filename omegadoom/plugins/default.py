# coding:utf-8

from datetime import datetime
import twisted.names.client
import urlparse

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase, OmegaDoomPluginRequest
from omegadoom.util import OmegaDoomUtil

class OmegaDoomPlugin(OmegaDoomPluginBase):

    commands = ['weather', 'ping', 'version', 'echo', 'dns', 'lol', 'karma']

    def run_command(self, protocol, command, data, privmsg):
        prefix, channel, message = privmsg
        nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
        nick_or_channel = nick if channel == self.config['nickname'] else channel

        if command == 'ping':
            self.requests[(command, nick)] = OmegaDoomPluginRequest(privmsg, datetime.now())
            protocol.ping(nick)

        elif command == 'weather':
            protocol.msg(nick_or_channel, 'Rain. :(')

        elif command == 'echo':
            protocol.msg(nick, message)

        elif command == 'karma':
            protocol.msg(nick_or_channel, '%s++' % (nick))

        elif command == 'dns':
            self.requests[(command, nick)] = OmegaDoomPluginRequest(privmsg, datetime.now())
            d = twisted.names.client.getHostByName(data)
            d.addBoth(self._dns_callback, protocol, prefix, data)
            
        elif command == 'lol':
            if data == '∞':
                protocol.msg(nick_or_channel, "All hail the loloboros!")
            else:
                lol_len = min(int(data), 42) - 1 if data.isdigit() else 0
                protocol.msg(nick_or_channel, "lol" + "ol"*lol_len)


    def _dns_callback(self, results, protocol, *args):
        prefix, hostname = args
        self.notify(protocol, 'dns', prefix, hostname, results) 


    def notify(self, protocol, event, *args):
        if event == 'pong':
            self._notify_pong(protocol, *args)
        elif event == 'dns':
            self._notify_dns(protocol, *args)
    

    def _notify_pong(self, protocol, *args):
        prefix, secs = args
        nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
      
        if ('ping', nick) in self.requests:
            privmsg, timestamp = self.requests[('ping', nick)]
            prefix, channel, message = privmsg
     
            nick_or_channel = nick if channel == self.config['nickname'] else channel
            protocol.msg(nick_or_channel, 'CTCP PING reply in %s secs' % (secs))

            del(self.requests[('ping', nick)])
            

    def _notify_dns(self, protocol, *args):
        prefix, hostname, ip = args
        nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
        
        if ('dns', nick) in self.requests:
            privmsg, timestamp = self.requests[('dns'), nick]
            prefix, channel, message = privmsg
     
            nick_or_channel = nick if channel == self.config['nickname'] else channel
            protocol.msg(nick_or_channel, '%s (%s)' % (hostname, ip))

            del(self.requests[('dns'), nick])

