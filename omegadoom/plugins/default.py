from datetime import datetime

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase
from omegadoom.util import OmegaDoomUtil


class OmegaDoomPlugin(OmegaDoomPluginBase):
  commands = ['ping', 'version']


  def setup(self):
    self._ping_requests = {}


  def run_command(self, protocol, command, data, privmsg):
    prefix, channel, message = privmsg
    nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)

    if command == 'ping':
      self._ping_requests[nick] = (privmsg, datetime.now())
      protocol.ping(nick)


  def notify(self, protocol, event, *args):
    if event == 'pong':
      prefix, secs = args
      nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
     
      print self._ping_requests

      if nick in self._ping_requests:
        privmsg, timestamp =  self._ping_requests[nick]
        prefix, channel, message = privmsg
       
        protocol.msg(nick if channel == self.config['nickname'] else channel,
                     'CTCP PING reply in %s secs' % (secs))



