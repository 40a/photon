********
Photon
********
Photon is a data driven tool designed to run workflows against an AZ using
Ansible.

A workflow is comprised of one more more playbooks, each configurable
with its own flags and options to be passed down to underlying call to
``ansible-playbook``. It supports the ability to resume a workflow from any
point in the event of a playbook failure.

Quick Start
===========
Create a file called ``photon.yml`` and define at least one AZ and workflow.

.. code-block:: yaml

    azs:
      proxmox:
        inventory: inventory/fusion/metapod/proxmox
    workflows:
      test_password_playbooks:
        playbooks:
          - path: playbooks/openstack/metapod/tests/percona_cinder.yml

.. important::
    ``azs.<name>.inventory`` is the only required value when defining an AZ.
    ``workflows.<name>.playbooks`` is the only required value when defining a
    workflow.

To execute a workflow against an AZ, simply run:

.. code-block:: bash

    $ photon --workflow test_password_playbooks --az proxmox

Environment Variables
=====================
Photon will use a copy of the existing environment to pass to its call to
``ansible-playbook``. This allows you to preserve your venv when using photon.
You can add to or overwrite environment variables in the ``azs.<name>.env``
section of your config.

.. code-block:: yaml

    azs:
      proxmox:
        inventory: inventory/fusion/metapod/proxmox
        # added to existing environment
        env:
          ANSIBLE_VAULT_PASSWORD_FILE: ~/.config/ansible-systems/vault-proxmox.pass

Workflow Flags
==============
Flags are simply CLI options that are passed to the underlying call to
``ansible-playbook``. When defined as ``workflows.<name>.flags`` they will be
applied to all playbooks in a workflow. When defined as
``workflows.<name>.playbooks.<playbook>.flags`` they will be applied only to
that specific playbook.

.. code-block:: yaml

    workflows:
      test_password_playbooks:
        flags:
          # applied to all playbooks in this workflow
          - --become
          - --connection=ssh
        playbooks:
          - path: playbooks/openstack/metapod/tests/percona_cinder.yml
            # applied to only this playbook
            flags:
              - --tags=tag1,tag2
              - --extra-vars=cinder_in_use=True

Limiting Execution
==================
By default, all workflows can be executed against all AZs. It is possible
to limit a workflow to only run against limited AZs. For example, a
workflow that tests password change playbooks makes sense against proxmox,
but would be destructive if run against a production AZ.

A workflow can be limited by adding the key ``workflows.<name>.allowed_azs``.

.. code-block:: yaml

    azs:
      proxmox:
        inventory: inventory/fusion/metapod/proxmox
      production:
        inventory: inventory/fusion/metapod/production
    workflows:
      test_password_playbooks:
        # will error if workflow is run against the az production
        allowed_azs:
          - proxmox
        playbooks:
          - path: playbooks/openstack/metapod/tests/percona_cinder.yml

Resuming Execution
==================
In the event of a playbook failure, photon will print a command as part of the
error message that can be used to continue the execution of a workflow from the
point where it failed. This is simply a list index that corresponds to the
position of a playbook in ``workflows.<workflow>.playbooks``.

.. code-block:: yaml

    workflows:
      test_password_playbooks:
        playbooks:
          - path: playbooks/openstack/metapod/tests/percona_cinder.yml
          - path: playbooks/openstack/metapod/tests/percona_keystone.yml
          - path: playbooks/openstack/metapod/tests/percona_glance.yml
          - path: playbooks/openstack/metapod/tests/percona_xtrabackup.yml

Using the above config, the command:

.. code-block:: bash

    $ photon --workflow test_password_playbooks --az proxmox --resume 3

Would resume execution starting with the ``percona_glance.yml`` playbook.
