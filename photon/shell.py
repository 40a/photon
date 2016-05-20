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
Photon CLI wrapper.
"""

import argparse

import photon
from photon import config
from photon import provisioner


def _parse_args():
    ap = argparse.ArgumentParser(prog='photon', description=__doc__.strip())
    ap.add_argument('--version', action='version', version=photon.__version__)
    sp = ap.add_subparsers(title='subcommands',
                           description='Valid subcommands',
                           help='Valid subcommands',
                           dest='subcmd')
    cp = sp.add_parser('converge', help='perform an ansible converge')
    cp.add_argument('--az', required=True, help='name of the az')

    args = ap.parse_args()
    return args


def main():
    args = _parse_args()
    c = config.Config(args.az)
    p = provisioner.Provisioner(c)
    print p._get_command()


if __name__ == '__main__':
    main()
