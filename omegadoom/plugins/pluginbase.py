import redis
from collections import namedtuple
from datetime import datetime
from twisted.internet.task import LoopingCall

OmegaDoomPluginRequest = namedtuple('PluginRequest', ['privmsg', 'timestamp'])

class OmegaDoomPluginBase(object):
    REQUEST_CLEANUP_INTERVAL = 60
    
    # list of commands this plugin handles
    commands = []


    def __init__(self, config):
        self._config = config
        self._redis = redis.Redis(host=config['redis_host'], port=config['redis_port'], db=0)
        
        self.requests = {}    
    
        self.setup()
        
        self._request_cleanup_lc = LoopingCall(self.request_cleanup)
        self._request_cleanup_lc.start(self.REQUEST_CLEANUP_INTERVAL)


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


    def request_cleanup(self):
        """ delete old requests, if any """
        self.requests = {k: v for k, v in self.requests.iteritems() if (datetime.now() - v.timestamp).total_seconds() >= self.REQUEST_CLEANUP_INTERVAL }
