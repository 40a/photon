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

from photon.ansible_playbook import AnsiblePlaybook


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
            a = AnsiblePlaybook()
            a.add_flag('inventory', self._config.inventory)
            a.add_flag('user', self._config.user)
            for f in self._config.flags:
                a.add_as_is(f)
            for f in d.get('extra_flags', []):
                a.add_as_is(f)
            a.add_as_is(playbook)
            if self._target:
                a.add_flag('limit', self._target, quoted=True)

            commands.append(a.bake)

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
