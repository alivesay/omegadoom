from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet.task import LoopingCall

from omegadoom.responder import OmegaDoomClientResponder

class OmegaDoomClient(irc.IRCClient):
  PING_INTERVAL = 300

  def __init__(self):
    self.quit_deferred = None
    self.timer = None


  def signedOn(self):
    print 'Signed on:', self.nickname
   
   nickserv_pass = self._ascii_get('nickserv_pass')
   if nickserv_pass:
     self.msg('nickserv', 'identify %s' % (nickserv_pass))

    for channel in self.config['channels']:
      self.join(channel.encode('ascii', 'ignored'))
      print 'Joined channel:', channel


  def privmsg(self, user, channel, msg):
    self.responder.privmsg(user, channel, msg)
  
  
  def connectionMade(self):
    irc.IRCClient.connectionMade(self)
    self.timer = LoopingCall(self._timer_callback)
    self.timer.start(self.PING_INTERVAL, False)
    print 'Connected:', self.config['network']


  def connectionLost(self, reason):
    irc.IRCClient.connectionLost(self, reason)
    self.timer.stop()

    if self.quit_deferred:
      self.quit_deferred.callback(None)

  
  def _timer_callback(self):
    self.ping(self.nickname)

  
  def pong(self, user, secs):
    self.responder.pong(user, secs)
    print 'CTCP PING reply from %s : %s seconds' % (user, secs)


  def _get_nickname(self):
    return self._ascii_get('nickname')
  nickname = property(_get_nickname)


  def _get_password(self):
    return self._ascii_get('password')
  password = property(_get_password)


  def _get_username(self):
    return self._ascii_get('username')
  username = property(_get_username)


  def _ascii_get(self, key):
    item = self.config.get(key)
    return item.encode('ascii', 'ignore') if item else None




class OmegaDoomClientFactory(protocol.Factory):
  protocol = OmegaDoomClient

  def __init__(self, config, plugin_manager):
    self.config = config
    self.plugin_manager = plugin_manager

  def buildProtocol(self, addr):
    p = self.protocol()
    p.factory = self
    p.config = self.config
    p.responder = OmegaDoomClientResponder(self.config, p, self.plugin_manager)
    
    return p

