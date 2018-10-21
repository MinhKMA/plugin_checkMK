from keystoneauth1 import session

from cinderclient.v3 import client as cinder_client
from keystoneclient.v3 import client as keystone_client
from glanceclient import Client as glance_client
from novaclient import client as nova_client
from neutronclient.v2_0 import client as neutron_client


class OpenstackClient(object):
    """Khởi tạo các client tới openstack bao gồm: keystone, nova, glance, neutron, cinder"""
    sess = None
    def __init__(self, session_auth=None):
        """Sử dụng openstack client kết nối openstack"""
        if session_auth is not None:
            self.sess = session.Session(auth=session_auth)

    @property
    def keystone_api(self):
        """Kết nối tới keystone"""
        return keystone_client.Client(session=self.sess)

    @property
    def nova_api(self):
        """Kết nối tới nova"""
        return nova_client.Client(version=2, session=self.sess)

    @property
    def glance_api(self):
        """Kết nối tới glance"""
        return glance_client('2', session=self.sess)

    @property
    def cinder_api(self):
        """Kết nối tới cinder"""
        return cinder_client.Client('3', session=self.sess)

    @property
    def neutron_api(self):
        """Kết nối tới neutron"""
        return neutron_client.Client(session=self.sess)
