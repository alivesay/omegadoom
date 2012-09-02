import json

class OmegaDoomConfigParser(object):
  DEFAULT_SCHEMA = [{'key': 'network',       'type': basestring, 'required': True},
                    {'key': 'port',          'type': int,        'required': True},
                    {'key': 'nickname',      'type': basestring, 'required': True},
                    {'key': 'channels',      'type': basestring, 'required': True,  'multivalued': True},
                    {'key': 'admins',        'type': basestring, 'required': True,  'multivalued': True},
                    {'key': 'nickserv_pass', 'type': basestring, 'required': False}]


  def __init__(self, schema = None):
    if schema is None:
      schema = self.DEFAULT_SCHEMA
      if self._validate_schema(schema):
        self._schema = schema
      else:
        raise ValueError('invalid schema')


  def _validate_schema(self, schema):
    return isinstance(schema, list) and all((isinstance(i, dict) and 'key' in i and 'type' in i for i in schema))


  def _validate_config(self, config, schema):
    for entry in schema:
      if entry['key'] in config:
        if entry.get('multivalued'):
          if not all((isinstance(item, entry['type']) for item in config[entry['key']])):
            raise TypeError("'%s' must be a list of type '%s'" % (entry['key'], entry['type']))
        elif not isinstance(config[entry['key']], entry['type']):
          raise TypeError("'%s' must be of type '%s'" % (entry['key'], entry['type']))
      elif entry.get('required'):
        raise KeyError("missing required attribute '%s'" % entry['key'])


  def load(self, filename):
    """ Loads a valid OmegaDoom config file as a dictionary. """

    with open(filename, 'r') as f:
      config = json.load(f)

    self._validate_config(config, self._schema)

    return config
