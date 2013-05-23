import imp
import glob
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from plugins.pluginbase import OmegaDoomPluginBase

class OmegaDoomPluginManagerFSEH(FileSystemEventHandler):
    def __init__(self, on_modified_callback):
        self._on_modified_callback = on_modified_callback
        
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            self._on_modified_callback(event.src_path)
    

class OmegaDoomPluginManager(object):

    def __init__(self, config):
        self._config = config
        self._plugin_path = os.path.join(os.path.dirname(__file__), 'plugins')
        self._plugins = {}
        self._commands = {}
            
        # load plugins
        for source in glob.glob(os.path.join(self._plugin_path, '*.py')):
            self._load_plugin(source)
        
        # start monitoring plugin directory for changes
        self._observer = Observer()
        self._fseh = OmegaDoomPluginManagerFSEH(self._load_plugin)
        self._observer.schedule(self._fseh, self._plugin_path, recursive=True)
        self._observer.start()


    def _load_plugin(self, filename):
        """ Loads source files containing valid OmegaDoom plugins. """

        basename, extension = os.path.splitext(os.path.basename(filename))
    
        try:
            if extension.lower() == '.py':
                with open(filename, 'r') as f:
                    module = imp.load_module(basename, f, filename, ('.py', 'r', imp.PY_SOURCE))
                    
                if hasattr(module, 'OmegaDoomPlugin'):
                    self._register_plugin(basename, filename, module.OmegaDoomPlugin(self._config)) 

        except Exception as e:
            print 'Error: OmegaDoomPlugin failed to load (%s): %s' % (str(e), filename)


    def _register_plugin(self, module, filename, instance):
        """ Removes old plugin references and registers new ones. """

        if not issubclass(type(instance), OmegaDoomPluginBase):
            raise Exception('Error: module \'%s\'is not a subclass of OmegaDoomPluginBase' % (module))

        # remove old references
        for key in self._commands.keys():
            if self._commands[key] == module:
                del(self._commands[key])
   
        # register commands
        for command in instance.commands:
            self._commands[command] = module

        self._plugins[module] = instance 

        print 'Loaded plugin: %s [%s]' % (module, ', '.join(instance.commands))


    def run_command(self, protocol, command, data, privmsg):
        # get protocol out of here an into a deferreda
        if command in self._commands:
            instance = self._plugins[self._commands[command]]
            try:
                instance.run_command(protocol, command, data, privmsg)
            except Exception as e:
                print 'Exception processing \'%s\':' % (str(e))

  
    def notify(self, protocol, event, *args):
        for module, instance in self._plugins.items():
            instance.notify(protocol, event, *args)
