import json

class OmegaDoomConfigParser(object):
  DEFAULT_SCHEMA = [{'key': 'network'},
                    {'key': 'port',          'type': int},
                    {'key': 'nickname'},
                    {'key': 'channels',      'multivalued': True},
                    {'key': 'admins',        'multivalued': True},
                    {'key': 'redis_host',    'required': False},
                    {'key': 'redis_port',    'type': int, 'required': False},
                    {'key': 'nickserv_pass', 'required': False},
                    {'key': 'command_char',  'required': True}]


  def __init__(self, schema = None):
    if schema is None:
      schema = self.DEFAULT_SCHEMA
      if self._validate_schema(schema):
        self._schema = schema


  def _validate_schema(self, schema):
    return isinstance(schema, list) and all((isinstance(i, dict) and 'key' in i for i in schema))


  def _validate_config(self, config, schema):
    for entry in schema:

      entry_key = entry['key']

      if entry_key in config:
        entry_type = entry.get('type', basestring)

        if entry.get('multivalued', False):
          
          if not all((isinstance(item, entry_type) for item in config[entry_key])):
            raise TypeError("'%s' must be a list of type '%s'" % (entry_key, entry_type))
        
        elif not isinstance(config[entry_key], entry_type):
          raise TypeError("'%s' must be of type '%s'" % (entry_key, entry_type))
      
      elif entry.get('required', True):
        raise KeyError("missing required attribute '%s'" % entry_key)


  def load(self, filename):
    """ Loads a valid OmegaDoom config file as a dictionary. """

    with open(filename, 'r') as f:
      config = json.load(f)

    self._validate_config(config, self._schema)

    return config
