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


@pytest.fixture()
def photon_config(photon_config_file):
    return config.Config('az', photon_config_file)


def test_invalid_az_raises(photon_config_file):
    with pytest.raises(config.ConfigException):
        config.Config('invalid', photon_config_file)


def test_deployment_version(photon_config):
    assert 'master' == photon_config.deployment_version


def test_inventory_version(photon_config):
    assert 'master' == photon_config.inventory_version


def test_playbook(photon_config):
    assert 'playbooks/openstack/metapod.yml' == photon_config.playbook


def test_inventory(photon_config):
    assert 'inventory/az' == photon_config.inventory


def test_user(photon_config):
    assert 'user' == photon_config.user


def test_az_user(photon_config):
    d = {'user': 'az_user'}
    photon_config._az_dict.update(d)

    assert 'az_user' == photon_config.user


def test_deployment_repo(photon_config):
    assert ('git@github.com:metacloud/ansible-systems.git' ==
            photon_config.deployment_repo)


def test_inventory_repo(photon_config):
    assert ('git@github.com:metacloud/ansible-inventory.git' ==
            photon_config.inventory_repo)


def test_flags(photon_config):
    expected = {
        'inventory': 'inventory/az',
        'user': 'user',
        'connection': 'ssh',
        'become': True
    }

    assert expected == photon_config.flags


def test_env(photon_config):
    expected = {
        'ANSIBLE_INVENTORY': 'inventory/az',
        'ANSIBLE_FORCE_COLOR': True,
        'ANSIBLE_HOST_KEY_CHECKING': False,
        'ANSIBLE_SSH_ARGS': ('-o UserKnownHostsFile=/dev/null '
                             '-o IdentitiesOnly=yes '
                             '-o ControlMaster=auto '
                             '-o ControlPersist=60s'),
    }

    assert expected == photon_config.env
