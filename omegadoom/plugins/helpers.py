# coding:utf-8

from datetime import timedelta
import gdata.youtube
import gdata.youtube.service
from gdata.service import RequestError
import urlparse
import re

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase, OmegaDoomPluginRequest
from omegadoom.util import OmegaDoomUtil

class OmegaDoomPlugin(OmegaDoomPluginBase):

    commands = ['youtube']
    matched_commands = { 'youtube': r'http:\/\/(?:www\.)?youtube.com\/watch\?(?=[^?]*v=\w+)(?:[^\s?]+)?' }
    
    yt_svc = gdata.youtube.service.YouTubeService()

    def run_command(self, protocol, command, data, privmsg):
        prefix, channel, message = privmsg
        nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
        nick_or_channel = nick if channel == self.config['nickname'] else channel

        if command == 'youtube':
            try:
                # TODO: needs deferred
                search = re.search(self.matched_commands[command], data)
                if search:
                    yt_url = urlparse.urlparse(search.group(0))
                    query = urlparse.parse_qs(yt_url.query)
                    video_id = query['v'][0]
                    entry = self.yt_svc.GetYouTubeVideoEntry(video_id=video_id)
                    if entry:
                        title = entry.media.title.text
                        duration = timedelta(seconds=int(entry.media.duration.seconds))
                        categories = ', '.join([c.text for c in entry.media.category])
                        protocol.msg(nick_or_channel, '[%s | %s | %s] - %s' % (title, duration, categories), 'https://youtu.be/%s' % video_id)
                else:
                    protocol.msg(nick_or_channel, '[Error: invalid video URL]')
                    
            except gdata.service.RequestError, inst:
                response = inst[0]
                protocol.msg(nick_or_channel, 'Error: %s (%s)' % (response['reason'], response['body']))
                
            except Exception as e:
                protocol.msg(nick_or_channel, '[Error: unhandled exception]' % e)
