
class OmegaDoomClientResponder(object):
  COMMAND_CHARACTER = '$'

  def __init__(self, config, protocol, plugin_manager):
    self._config = config
    self._protocol = protocol 
    self._plugin_manager = plugin_manager


  def privmsg(self, prefix, channel, message):
    print prefix, channel, message
  
    if message.startswith(self.COMMAND_CHARACTER):
      command = message.split(' ')[0][1:]
      data = message[message.find(command) + len(command):].strip()
      
      if command:
        self._plugin_manager.run_command(self._protocol,
                                         command,
                                         data,
                                         (prefix, channel, message))

  def notify(self, event, *args):
    self._plugin_manager.notify(self._protocol, event, *args)

