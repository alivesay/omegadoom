
class OmegaDoomMessage(object):

  def __init__(self, message, config):
    if message.startswith(self.COMMAND_CHARACTER):
      command = message.split(' ')[0][1:]
      data = message[message.find(command) + len(command):].strip()

    
