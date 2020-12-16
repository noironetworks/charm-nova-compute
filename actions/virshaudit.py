#!/usr/bin/env python3
#
# Copyright 2020 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

_path = os.path.dirname(os.path.realpath(__file__))
_hooks = os.path.abspath(os.path.join(_path, '../hooks'))


def _add_path(path):
    if path not in sys.path:
        sys.path.insert(1, path)


_add_path(_hooks)


import subprocess
from charmhelpers.core import hookenv


def virsh_audit():
    """
    Return the list of VM instances as virsh sees on the
    compute node
    """
    outmap = {}
    cmd = "virsh list --all"
    try:
        outmap['virsh-domains'] = subprocess.check_output(
            cmd, shell=True).decode('UTF-8')
    except subprocess.CalledProcessError as e:
        hookenv.log(e)
        hookenv.action_fail(
            "Getting virsh list report failed: {}".format(e.message)
        )
    hookenv.action_set(outmap)


if __name__ == '__main__':
    virsh_audit()
