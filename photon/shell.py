# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2017 Cisco Systems
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
from __future__ import print_function

import argparse

import photon
from photon import config
from photon import provisioner

ap = argparse.ArgumentParser(prog='photon', description=__doc__.strip())
ap.add_argument('--version', action='version', version=photon.__version__)
rp = ap.add_argument_group('required arguments')
rp.add_argument('--az', required=True, help='name of the availability zone')
rp.add_argument('--workflow',
                required=True,
                help='name of the workflow to perform')
ap.add_argument('--config',
                default='photon.yml',
                help='path to the photon config')
ap.add_argument('--resume',
                default=1,
                help='playbook position to start at within workflow')
args = ap.parse_args()


def main():
    try:
        c = config.Config(az=args.az,
                          workflow=args.workflow,
                          config_file=args.config)
    except photon.config.ConfigError as e:
        ap.error(e)

    p = provisioner.Provisioner(c)
    p.run(args.resume)


if __name__ == '__main__':
    main()
