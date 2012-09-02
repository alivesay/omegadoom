import random, re

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase
from omegadoom.util import OmegaDoomUtil

class OmegaDoomPlugin(OmegaDoomPluginBase):
  commands = ['roll', 'exp', 'inventory']


  def run_command(self, protocol, command, data, privmsg):
    prefix, channel, message = privmsg
    nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)

    if command == 'roll':
      if data:
        # http://stackoverflow.com/questions/1031466/evaluate-dice-rolling-notation-strings
        f=lambda s:sum(int(c or 0)+sum(random.randint(1,int(b))for i in[0]*int(a or 1))for a,b,c in re.findall(r'(\d*)d(\d+)(\s*[+-]\s*\d+)?',s))
        protocol.msg(nick if channel == self.config['nickname'] else channel, str(f(data)))
