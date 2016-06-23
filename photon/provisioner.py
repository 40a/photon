# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2016 Cisco Systems
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
A class responsible for construct the proper ``ansible-playbook`` commands.
"""
from __future__ import print_function

import sys

import colorama


class Provisioner(object):
    def __init__(self, config, action, target=None):
        self._config = config
        self._action = action
        self._target = target
        colorama.init(autoreset=True)

    def _get_commands(self):
        """ Generates and returns a list of lists containing the commands
        the provisioner will consume.

        :return: list
        """
        d = self._config.workflows.get(self._action, {})

        commands = []
        for playbook in d.get('playbooks', []):
            cmd = [
                'ansible-playbook',
                self._get_flag('inventory', self._config.inventory),
                self._get_flag('user', self._config.user),
                self._config.flags,
                d.get('extra_flags', []),
                playbook,
            ]
            if self._target:
                target = self._get_flag('limit', self._target, quoted=True)
                cmd.extend([target])

            commands.append(self._flatten(cmd))

        return commands

    def run(self):
        msg = '{}*** Ansible commands to verify ***'.format(
            colorama.Fore.YELLOW)
        print(msg, file=sys.stderr)
        print(file=sys.stderr)
        env = ['{}={}'.format(k, v) for k, v in self._config.env.iteritems()]
        for command in self._get_commands():
            print(' '.join(env), end=' ')
            print(' '.join(command))

    # Taken from compiler/ast, since deprecated in python 3
    def _flatten(self, seq):
        l = []
        for elt in seq:
            t = type(elt)
            if t is tuple or t is list:
                for elt2 in self._flatten(elt):
                    l.append(elt2)
            else:
                l.append(elt)
        return l

    def _get_flag(self, flag, value, quoted=False):
        if quoted:
            return "--{}=\'{}\'".format(flag, value)
        else:
            return '--{}={}'.format(flag, value)
