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

from photon import config


def test_inventory(photon_config):
    assert 'inventory/az' == photon_config.inventory


def test_az_inventory(photon_config_file):
    c = config.Config('az/test', photon_config_file)

    assert 'az_inventory' == c.inventory


def test_user(photon_config):
    assert '$USER' == photon_config.user


def test_flags(photon_config):
    expected = ['--become', '--connection=ssh']

    assert expected == photon_config.flags


def test_env(photon_config):
    expected = {}

    assert expected == photon_config.env


def test_env_az(photon_config_file):
    c = config.Config('az/env_test', photon_config_file)
    expected = {'ANSIBLE_HOST_KEY_CHECKING': False,
                'ANSIBLE_INSTRUMENT_MODULES': True,
                'ANSIBLE_SSH_ARGS': '"-F $HOME/.axion/ssh_config"'}

    assert expected == c.env


def test_workflows(photon_config):
    w = photon_config.workflows

    assert len(w) == 3
