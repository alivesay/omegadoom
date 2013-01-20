import redis

from omegadoom.util import OmegaDoomUtil

class OmegaDoomPluginBase(object):
  # list of commands this plugin handles
  commands = []


  def __init__(self, config):
    self._config = config
    self._redis = redis.Redis(host='localhost', port=6739, db=0)
    self.setup()


  def _get_config(self):
    return self._config
  config = property(_get_config)

 
  # called by __init__
  def setup(self):
    pass


  # called when a command registered to this plugin is received 
  def run_command(self, protocol, command, data, privmsg):
    # prefix, channel, message = privmsg
    # nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)
    pass
 

  def notify(self, protocol, event, *args):
    pass



