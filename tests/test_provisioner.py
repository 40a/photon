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

import pytest

from photon import config
from photon import provisioner


@pytest.fixture()
def photon_config(photon_config_file):
    return config.Config('az', photon_config_file)


@pytest.fixture()
def photon_provisioner(photon_config):
    return provisioner.Provisioner(photon_config)


def test_get_command(photon_provisioner):
    result = photon_provisioner._get_command()
    expected = ['ansible-playbook', '--become', '--connection=ssh',
                '--inventory=inventory/az', '--user=user']

    assert expected == result


def test_get_flags(photon_provisioner):
    d = {'foo_bar': 'baz', 'qux': True}

    assert ['--foo-bar=baz', '--qux'] == photon_provisioner._get_flags(d)
