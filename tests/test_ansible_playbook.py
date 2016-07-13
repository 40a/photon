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


def test_bake(ansible_playbook):
    assert ['ansible-playbook'] == ansible_playbook.bake


def test_add_flag(ansible_playbook):
    ansible_playbook.add_flag('foo', 'bar')

    assert ['ansible-playbook', '--foo=bar'] == ansible_playbook._command


def test_add_flag_with_quoted(ansible_playbook):
    ansible_playbook.add_flag('foo', 'bar', quoted=True)

    assert ['ansible-playbook', "--foo='bar'"] == ansible_playbook._command


def test_add_argument(ansible_playbook):
    ansible_playbook.add_argument('foo')
    ansible_playbook.add_argument('bar')
    ansible_playbook.add_argument('--baz')

    assert ['ansible-playbook', 'foo', 'bar', '--baz'
            ] == ansible_playbook._command
