from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import defer, reactor

from omegadoom.configparser import OmegaDoomConfigParser
from omegadoom.client import OmegaDoomClientFactory
from omegadoom.pluginmanager import OmegaDoomPluginManager

class OmegaDoomModel(object):

  def __init__(self, version):
    self.version = version
    self.protocol = None
    self.config = None

    self.reactor = reactor
    self.reactor.addSystemEventTrigger('before', 'shutdown', self._shutdown)


  def _shutdown(self):
    quit_deferred = defer.Deferred()
    self.protocol.quit_deferred = quit_deferred

    self.protocol.quit('And death shall have no dominion.')

    return quit_deferred


  def reprogram(self, config):

    config_parser = OmegaDoomConfigParser()
    self.config = config_parser.load(config)


  def boot(self):
    if not self.config:
      raise Exception('These hybrid models are real killers -- better reprogram first!')

    endpoint = TCP4ClientEndpoint(self.reactor,
                                  self.config['network'],
                                  self.config['port'])

    plugin_manager = OmegaDoomPluginManager(self.config)   
    factory = OmegaDoomClientFactory(self.config, plugin_manager)
    connect_deferred = endpoint.connect(factory)
    connect_deferred.addCallbacks(self._callback_connected, self._callback_error)

    self.reactor.run()

  def _callback_connected(self, protocol):
    self.protocol = protocol


  def _callback_error(self, reason):
    raise Exception(reason)

