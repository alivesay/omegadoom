import re

class OmegaDoomUtil(object):
  _PREFIX_REGEX = re.compile("(?P<nick>.*?)!(?P<ident>.*?)@(?P<host>.*)")


  @staticmethod
  def parse_prefix(prefix):
    return OmegaDoomUtil._PREFIX_REGEX.match(prefix).group('nick', 'ident', 'host')

