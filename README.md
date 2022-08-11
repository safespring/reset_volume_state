# Reset volume state

This is a simple CLI helper for resetting volumes stuck in a "reserved" state, a
bug we frequently see with Kubernetes clients when detaching and attaching
volumes rapidly. It will iterate over volumes in a project and change from
"reserved" to "available" if the volume has no attachments - indicating an
incorrect state. Please note that this is a temporary workaround and will not
be needed once we've addressed the underlying problem.

## Installation

The script requires a Python 3 runtime. A virtual environment is recommended.
Clone the following repository where you intend to run the script and install
the requirements:

```
git clone https://github.com/safespring/reset_volume_state
pip install -r requirements -e .
```

## Usage

The policy allowing a non-admin user to reset the volume's state is limited to
the owner of the volume, meaning the user that created it (this is visible in
the user_id field). Other project members - even if project admins - are not
allowed to make the request.

To use the script you need a clouds.yaml configuration file in order to connect
to the Openstack API, e.g.

```
clouds:
  your_project_name:
    region_name: sto1
    interface: public
    auth:
      auth_url: https://v2.dashboard.sto1.safedc.net:5000/v3
      password: your_password
      project_domain_name: your_domain_name
      project_name: project.domain.com
      user_domain_name: users
      username: owner@domain.com
```

If you're not familiar with using a yaml configuration, please read https://docs.openstack.org/python-openstackclient/train/cli/man/openstack.html#cloud-configuration

Before you run the reset script, please verify that **every** volume in the project
with the "reserved" state are actually stuck and needs a reset. There may be
situations where "reserved" is the desired state for a volume for short amount
of time. Although this script will not do any operations on the actual volume
(it only changes the state flag in the database from "reserved" to "available"),
doing so in a middle of an ongoing operation might break things and require
technical support from an admin in order to solve. **Use at your own risk!**

To list all volumes in a project, use the openstack CLI:

```
openstack --os-cloud your_project_name volume list
```

Look for volumes with a "reserved" state and no attachments. If these are all
stuck volumes, you're ready to run the script:

```
python3 reset_volume_state.py --cloud your_project_name
```

Then verify that they all have changed to "available" by running:

```
openstack --os-cloud your_project_name volume list
```

once more.

Please note that the script is silent by default. You may enable debug mode by
adding the following flag:

```
python3 reset_volume_state.py --cloud your_project_name --debug
```
