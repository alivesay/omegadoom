import random
import re
import redis
from collections import namedtuple

from omegadoom.plugins.pluginbase import OmegaDoomPluginBase
from omegadoom.util import OmegaDoomUtil


def roll(notation):
    # http://stackoverflow.com/questions/1031466/evaluate-dice-rolling-notation-strings
    f=lambda s:sum(int(c or 0)+sum(random.randint(1,int(b))for i in[0]*int(a or 1))for a,b,c in re.findall(r'(\d*)d(\d+)(\s*[+-]\s*\d+)?',s))
    return f(notation)

OmegaDoomRPGPlayer = namedtuple('RPGPlayer', ['credits'])
OmegaDoomRPGWeapon = namedtuple('RPGWeapons', ['damage', 'cost'])

players = {}

weapons = { 'pair of fists' : OmegaDoomRPGWeapon(1, 0),
            'stick' : OmegaDoomRPGWeapon(2, 50),
            'glowing sword' : OmegaDoomRPGWeapon(3, 100) }

class OmegaDoomPlugin(OmegaDoomPluginBase):

    commands = ['roll', 'exp', 'inventory', 'search']

    def run_command(self, protocol, command, data, privmsg):
        prefix, channel, message = privmsg
        nick, ident, host = OmegaDoomUtil.parse_prefix(prefix)

        target = nick if channel == self.config['nickname'] else channel

        if command == 'inventory':
            protocol.msg(target, 'Not implemented yet.')

        if command == 'roll':
            if data:
                protocol.msg(target, str(roll(data)))

        if command == 'search':
            search_check = roll('1d10')
            if search_check <= 2:
                w = random.choice(list(weapons.keys()))
                protocol.msg(target, 'You found a %s!' % (w))
            elif search_check <= 5:
                player_credits = roll('1d100')
                protocol.msg(target, 'You found %s credits!' % (player_credits))
            else:
                protocol.msg(target, 'You found... nothing.')
