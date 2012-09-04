
class OmegaDoomClientResponder(object):
  COMMAND_CHARACTER = '$'

  def __init__(self, config, protocol, plugin_manager):
    self._config = config
    self._protocol = protocol 
    self._plugin_manager = plugin_manager


  def privmsg(self, user, channel, msg):
    print user, channel, msg
  
    if msg.startswith(self.COMMAND_CHARACTER):
      command = msg.split(' ')[0][1:]
      data = msg[msg.find(command) + len(command):].strip()
      
      if command:
        self._plugin_manager.run_command(self._protocol,
                                         command,
                                         data,
                                         (user, channel, msg))

    
  def pong(self, user, secs):
    self._plugin_manager.notify(self._protocol, 'pong', user, secs)
    
