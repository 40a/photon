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

import yaml
"""
A class responsible for handling configuration, and provide the data needed
to construct a proper ``ansible-playbook`` command.
"""


class ConfigException(Exception):
    pass


class Config(object):
    def __init__(self, az, config='./photon.yml'):
        self._az = az
        self._config = config
        self._config_dict = self._get_config()
        self._az_dict = self._get_az_config()

    @property
    def deployment_version(self):
        return self._az_dict.get('ansible_deployment_version')

    @property
    def inventory_version(self):
        return self._az_dict.get('ansible_inventory_version')

    @property
    def playbook(self):
        return self._config_dict.get('playbook')

    @property
    def inventory(self):
        return self._config_dict.get('inventory').format(az=self._az)

    @property
    def user(self):
        u = self._config_dict.get('user')

        return self._az_dict.get('user', u)

    @property
    def deployment_repo(self):
        return self._config_dict.get('deployment_repo')

    @property
    def inventory_repo(self):
        return self._config_dict.get('inventory_repo')

    @property
    def env(self):
        d = self._config_dict.get('env')
        d['ANSIBLE_INVENTORY'] = self.inventory

        return d

    @property
    def flags(self):
        d = self._config_dict.get('flags')
        d['inventory'] = self.inventory
        d['user'] = self.user

        return d

    def _get_az_config(self):
        d = self._config_dict.get(self._az)
        if d is None:
            msg = "'{}' az missng from the config file".format(self._az)
            raise ConfigException(msg)

        return d

    def _get_config(self):
        with open(self._config) as stream:
            return yaml.load(stream)
