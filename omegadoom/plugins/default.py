from datetime import datetime

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase
from omegadoom.util import OmegaDoomUtil


class OmegaDoomPlugin(OmegaDoomPluginBase):

  commands = ['ping', 'version', 'echo']


  def setup(self):
    self._ping_requests = {}


  def run_command(self, protocol, command, data, privmsg):
    prefix, channel, message = privmsg
    nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
    nick_or_channel = nick if channel == self.config['nickname'] else channel

    if command == 'ping':
      self._ping_requests[nick] = (privmsg, datetime.now())
      protocol.ping(nick)

    elif command == 'echo':
      protocol.msg(nick_or_channel, message)


  def notify(self, protocol, event, *args):
    if event == 'pong':
      self._notify_pong(protocol, *args)
    

  def _notify_pong(self, protocol, *args):
      prefix, secs = args
      nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
      
      if nick in self._ping_requests:
        privmsg, timestamp = self._ping_requests[nick]
        prefix, channel, message = privmsg
       
        nick_or_channel = nick if channel == self.config['nickname'] else channel
        protocol.msg(nick_or_channel, 'CTCP PING reply in %s secs' % (secs))

        del(self._ping_requests[nick])

        # delete old requests, if any
        now = datetime.now()
        for k,v in self._ping_requests.items():
          if (now - v[1]).seconds > 60:
            del(self._ping_requests[k])
