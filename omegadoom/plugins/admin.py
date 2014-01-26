from twisted.internet import reactor

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase
from omegadoom.util import OmegaDoomUtil

class OmegaDoomPlugin(OmegaDoomPluginBase):

  commands = ['join', 'leave', 'quit', 'say']

  def run_command(self, protocol, command, data, privmsg):
    prefix, channel, message = privmsg
    nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
    nick_or_channel = nick if channel == self.config['nickname'] else channel

    if nick not in self.config['admins']:
      protocol.msg(nick_or_channel, 'Access denied.')
      return

    if command == 'join':
      if data:
        protocol.join(data)
        print 'Joined channel: ', data

    elif command == 'leave':
      if data:
        protocol.leave(data)
        print 'Left channel: ', data

    elif command == 'quit':
      reactor.stop()

    elif command == 'say':
      if data:
        protocol.msg(nick_or_channel, data)
      
