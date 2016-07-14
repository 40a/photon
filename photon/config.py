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
to construct the proper ``ansible-playbook`` commands.
"""


class Config(object):
    def __init__(self, az, config='photon.yml'):
        self._az = az
        self._config = config
        self._config_dict = self._get_config()
        self._az_dict = self._get_az_config()

    @property
    def inventory(self):
        """ Return the path to inventory.  The inventory can be overriden in
        the ``az`` section of the config.

        :return: str
        """
        i = self._config_dict.get('inventory')
        fi = self._az_dict.get('inventory', i)

        return fi.format(az=self._az)

    @property
    def user(self):
        return self._config_dict.get('user')

    @property
    def flags(self):
        """ Return and list of command line flags used by the provisioner.

        :return: list
        """
        return sorted(self._config_dict.get('flags'))

    @property
    def env(self):
        """ Return an environment dict used by the provisioner.  The
        environment can be overriden in the ``az`` section of the config.

        :return: dict
        """
        e = self._config_dict.get('env', {})

        return self._az_dict.get('env', e)

    @property
    def workflows(self):
        return self._config_dict.get('workflows')

    def _get_az_config(self):
        d = self._config_dict.get('azs', {})

        return d.get(self._az, {})

    def _get_config(self):
        with open(self._config) as stream:
            return yaml.safe_load(stream)
