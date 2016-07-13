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

import copy

import pytest

from photon import config
from photon import provisioner


@pytest.fixture()
def base_command():
    return ['ansible-playbook', '--inventory=inventory/az', '--user=user',
            '--become', '--connection=ssh']


@pytest.fixture()
def command_with_extra_flags(base_command):
    cmd = copy.copy(base_command)
    cmd.extend(['--extra-vars="skip_handlers=True"',
                '--extra-vars="openstack_serial_controller=1"',
                '--skip-tags="functional_tests,integration_tests"'])

    return cmd


def test_get_commands(photon_provisioner):
    assert [] == photon_provisioner._get_commands()


def test_extra_flags_missing(photon_config_file, base_command, mocked_user):
    c = config.Config('az', photon_config_file)
    p = provisioner.Provisioner(c, 'restart')
    result = p._get_commands()

    expected = copy.copy(base_command)
    expected.extend(['playbooks/openstack/metapod/service_restart.yml'])

    assert expected == result[0]


def test_upgrade_workflow(photon_config, command_with_extra_flags,
                          mocked_user):
    p = provisioner.Provisioner(photon_config, 'upgrade')
    result = p._get_commands()

    expected = copy.copy(command_with_extra_flags)
    expected.extend(['playbooks/openstack/metapod/package_upgrade.yml'])

    assert expected == result[0]

    expected = copy.copy(command_with_extra_flags)
    expected.extend(['playbooks/openstack/metapod.yml'])

    assert expected == result[1]


def test_upgrade_workflow_with_limit(photon_config, command_with_extra_flags,
                                     mocked_user):
    p = provisioner.Provisioner(photon_config, 'upgrade', 'mcp[1]')
    result = p._get_commands()

    expected = copy.copy(command_with_extra_flags)
    expected.extend(['playbooks/openstack/metapod/package_upgrade.yml'])
    expected.extend(["--limit='mcp[1]'"])

    assert expected == result[0]


def test_restart_workflow(photon_config, base_command, mocked_user):
    p = provisioner.Provisioner(photon_config, 'restart')
    result = p._get_commands()

    expected = copy.copy(base_command)
    expected.extend(['playbooks/openstack/metapod/service_restart.yml'])

    assert expected == result[0]
