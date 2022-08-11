import openstack
import click
import logging
import sys

LOG = logging.getLogger(__name__)

def find_and_reset_volume_state(os):

    volumes = os.list_volumes()

    for v in volumes:
        if not v.attachments and v.status == 'reserved':
            LOG.debug("Resetting state of volume {}".format(v.id))
            os.session.post('/volumes/' + v.id + '/action',
                            json={'os-reset_status': {'status': 'available'}},
                            microversion_service_type='volume',
                            endpoint_filter={'service_type': 'block-storage', 'interface': 'public', 'min_version': '3', 'max_version': 'latest'})


@click.command()
@click.option('--cloud', required=True, help='Name of the cloud to connect to')
@click.option('--debug', is_flag=True, default=False, help='Enable debug logging')
def main(cloud, debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    os = openstack.connect(cloud=cloud)
    LOG.debug("Connected to cloud {}".format(os.name))
    find_and_reset_volume_state(os)
    sys.exit(0)


if __name__ == '__main__':
    main()
