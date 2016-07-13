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

import os

import pytest

from photon import config
from photon import provisioner
from photon.ansible_playbook import AnsiblePlaybook


@pytest.fixture()
def photon_config(photon_config_file):
    return config.Config('az', photon_config_file)


@pytest.fixture()
def photon_provisioner(photon_config):
    return provisioner.Provisioner(photon_config, None)


@pytest.fixture()
def ansible_playbook():
    return AnsiblePlaybook()


@pytest.fixture()
def photon_config_content():
    return """
---
inventory: inventory/{az}
flags:
  - --connection=ssh
  - --become
env: {}
azs:
  az/test:
    inventory: az_inventory
  az/env_test:
    env:
      ANSIBLE_HOST_KEY_CHECKING: False
      ANSIBLE_INSTRUMENT_MODULES: True
      ANSIBLE_SSH_ARGS: '"-F $HOME/.axion/ssh_config"'
workflows:
  upgrade:
    extra_flags:
      - --extra-vars="skip_handlers=True"
      - --extra-vars="openstack_serial_controller=1"
      - --skip-tags="functional_tests,integration_tests"
    playbooks:
      - playbooks/openstack/metapod/package_upgrade.yml
      - playbooks/openstack/metapod.yml
  restart:
    playbooks:
      - playbooks/openstack/metapod/service_restart.yml
  deploy:
    playbooks:
      - playbooks/openstack/metapod.yml
"""


@pytest.fixture()
def photon_config_file(photon_config_content, tmpdir, request):
    d = tmpdir.mkdir('photon')
    c = d.join(os.extsep.join(('photon', 'yml')))
    c.write(photon_config_content)

    def cleanup():
        os.remove(c.strpath)
        os.rmdir(d.strpath)

    request.addfinalizer(cleanup)

    return c.strpath


@pytest.fixture()
def mocked_user(monkeypatch):
    def mockreturn():
        return {'USER': 'user'}

    return monkeypatch.setattr(os, 'environ', mockreturn())
