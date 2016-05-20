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


class Provisioner(object):
    def __init__(self, config):
        self._config = config

    def _get_command(self):
        """ Generates and returns a string which the provisioner invokes.
        :return: str
        """
        flags = self._config.flags

        cmd = []
        cmd.extend(['ansible-playbook'])
        cmd.extend(self._get_flags(flags))

        return cmd

    def _get_flags(self, d):
        return ['--{}={}'.format(k, v) if v else '--{}'.format(k)
                for k, v in self._flags_generator(d)]

    def _flags_generator(self, d):
        for k in sorted(d.iterkeys()):
            v = d[k]
            k = k.replace('_', '-')
            if v is True:
                yield k, None
            else:
                yield k, v
