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
from photon import provisioner
from tests import helper


class TestProvisioner(testtools.TestCase):
    def setUp(self):
        super(TestProvisioner, self).setUp()
        self._photon_config = helper.get_photon_config()
        self._config = config.Config('az', self._photon_config.name)
        self._provisioner = provisioner.Provisioner(self._config)

    def tearDown(self):
        super(TestProvisioner, self).tearDown()
        self._photon_config.close()

    def test_get_command(self):
        result = self._provisioner._get_command()
        expected = ['ansible-playbook', '--become', '--connection=ssh',
                    '--inventory=inventory/{az}', '--user=todo']

        self.assertEquals(expected, result)

    def test_get_flags(self):
        d = {'foo_bar': 'baz', 'qux': True}

        assert ['--foo-bar=baz', '--qux'] == self._provisioner._get_flags(d)
