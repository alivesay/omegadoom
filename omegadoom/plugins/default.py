# coding:utf-8

from datetime import datetime
import twisted.names.client
import gdata.youtube
import gdata.youtube.service

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase, OmegaDoomPluginRequest
from omegadoom.util import OmegaDoomUtil

class OmegaDoomPlugin(OmegaDoomPluginBase):

    commands = ['ping', 'version', 'echo', 'dns', 'lol']

    yt_svc = gdata.youtube.service.YouTubeService()

    def run_command(self, protocol, command, data, privmsg):
        prefix, channel, message = privmsg
        nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
        nick_or_channel = nick if channel == self.config['nickname'] else channel

        if command == 'ping':
            self.requests[(command, nick)] = OmegaDoomPluginRequest(privmsg, datetime.now())
            protocol.ping(nick)

        elif command == 'echo':
            protocol.msg(nick, message)

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
        
        elif command == 'youtube':
            try:
                yt_url = urlparse.urlparse(data)
                query = urlparse.parse_qs(yt_url.query)
                video_id = query["v"][0]
                entry = self.yt_svc.GetYouTubeVideoEntry(video_id=video_id)
                if entry:
                    protocol.msg(nick_or_channel, "[%s]" % (entry.media.title.text))
            except:
                protocol.msg(nick_or_channel, "[Error: bad url]")



    def _dns_callback(self, results, protocol, *args):
        prefix, hostname = args
        self._notify_dns(protocol, prefix, hostname, results) 


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
        
        if nick in self._dns_requests:
            privmsg, timestamp = self._dns_requests[nick]
            prefix, channel, message = privmsg
     
            nick_or_channel = nick if channel == self.config['nickname'] else channel
            protocol.msg(nick_or_channel, '%s (%s)' % (hostname, ip))

            del(self._dns_requests[nick])
