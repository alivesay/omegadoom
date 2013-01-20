from twisted.internet import reactor

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase

class OmegaDoomPlugin(OmegaDoomPluginBase):

  commands = ['join', 'leave', 'quit']
  
  def __init__(self, config):
    OmegaDoomPluginBase.__init__(self, config)


  def run_command(self, protocol, command, data, privmsg):
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
