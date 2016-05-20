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

import tempfile


def get_photon_config():
    config = """
---
playbook: playbooks/openstack/metapod.yml
inventory: inventory/{az}
user: user
deployment_repo: git@github.com:metacloud/ansible-systems.git
inventory_repo: git@github.com:metacloud/ansible-inventory.git
flags:
  connection: ssh
  become: True
env:
  ANSIBLE_FORCE_COLOR: True
  ANSIBLE_HOST_KEY_CHECKING: False
  ANSIBLE_SSH_ARGS: >-
    -o UserKnownHostsFile=/dev/null
    -o IdentitiesOnly=yes
    -o ControlMaster=auto
    -o ControlPersist=60s
az:
  deployment_version: master
  inventory_version: master
"""

    f = tempfile.NamedTemporaryFile()
    f.write(config)
    f.flush()

    return f
