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
"""
A class responsible for managing ``ansible-playbook`` commands.
"""


class AnsiblePlaybook(object):
    def __init__(self):
        self._command = ['ansible-playbook']

    @property
    def bake(self):
        return self._command

    def add_flag(self, flag, value, quoted=False):
        """
        Adds command line flags to the ansible command managed internally
        by `self._command`.

        :return: None
        """
        flag = self._get_flag(flag, value, quoted)
        self._add(flag)

    def add_argument(self, argument):
        """
        Adds command line arguments as-is to the ansible command managed
        internally by `self._command`.

        :return: None
        """
        self._add(argument)

    def _add(self, argument):
        self._command.extend([argument])

    def _get_flag(self, flag, value, quoted):
        """
        Constructs and returns command line flag string.  The value can
        optionally be quoted.

        :return: str
        """
        if quoted:
            return "--{}=\'{}\'".format(flag, value)
        else:
            return '--{}={}'.format(flag, value)
