# coding:utf-8

from datetime import timedelta
import gdata.youtube
import gdata.youtube.service
from gdata.service import RequestError
import urlparse
import re
import urllib
import urllib2
import json

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase, OmegaDoomPluginRequest
from omegadoom.util import OmegaDoomUtil

class OmegaDoomPlugin(OmegaDoomPluginBase):

    commands = ['youtube', 'tts']
    matched_commands = { 'youtube': r'https?:\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?' }
#    matched_commands = { 'youtube': r'https?:\/\/(?:www\.)?youtube.com\/watch\?(?=[^?]*v=\w+)(?:[^\s?]+)?' }
    
    yt_svc = gdata.youtube.service.YouTubeService()

    def run_command(self, protocol, command, data, privmsg):
        prefix, channel, message = privmsg
        nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
        nick_or_channel = nick if channel == self.config['nickname'] else channel

        if command == 'youtube':
            try:
                # TODO: needs deferred
                url_matches = re.findall(self.matched_commands[command], data)
                if url_matches:
                    for url in url_matches:
                        video_id = url[0]

			if len(url) > 0 and url[0]: 
                            entry = self.yt_svc.GetYouTubeVideoEntry(video_id=video_id)
			else:
                            return

                        if entry:
                            title = entry.media.title.text
                            duration = timedelta(seconds=int(entry.media.duration.seconds))
                            categories = ', '.join([c.text for c in entry.media.category])
                            protocol.msg(nick_or_channel, '[%s | %s | %s] - %s' % (title, duration, categories, 'http://y2u.be/%s' % video_id))
                else:
                    protocol.msg(nick_or_channel, '[Error: invalid video URL]')
                    
            except gdata.service.RequestError, inst:
                response = inst[0]
                protocol.msg(nick_or_channel, 'Error: %s (%s)' % (response['reason'], response['body']))
                
            except Exception as e:
                protocol.msg(nick_or_channel, '[Error: unhandled exception]' % e)


        elif command == 'tts':
            tts_url = 'http://tts-api.com/tts.mp3?q=%s' % data
            req = urllib2.Request('http://tinyurl.com/api-create.php','url=%s' % urllib.quote(tts_url))
            results = urllib2.urlopen(req)
            say_url = results.read()
            protocol.msg(nick_or_channel, say_url)
