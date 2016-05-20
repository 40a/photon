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

import testtools

from photon import config
from tests import helper


class TestConfig(testtools.TestCase):
    def setUp(self):
        super(TestConfig, self).setUp()
        self._photon_config = helper.get_photon_config()
        self._config = config.Config('az', self._photon_config.name)

    def tearDown(self):
        super(TestConfig, self).tearDown()
        self._photon_config.close()

    def test_deployment_version(self):
        self.assertEquals('master', self._config.deployment_version)

    def test_inventory_version(self):
        self.assertEquals('master', self._config.inventory_version)

    def test_playbook(self):
        self.assertEquals('playbooks/openstack/metapod.yml',
                          self._config.playbook)

    def test_flags(self):
        expected = {
            'inventory': 'inventory/{az}',
            'user': 'todo',
            'connection': 'ssh',
            'become': True
        }

        self.assertDictEqual(expected, self._config.flags)

    def test_env(self):
        expected = {
            'ANSIBLE_FORCE_COLOR': True,
            'ANSIBLE_HOST_KEY_CHECKING': False,
            'ANSIBLE_SSH_ARGS': ('-o UserKnownHostsFile=/dev/null '
                                 '-o IdentitiesOnly=yes '
                                 '-o ControlMaster=auto '
                                 '-o ControlPersist=60s'),
        }

        self.assertDictEqual(expected, self._config.env)
