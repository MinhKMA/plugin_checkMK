#!/usr/bin/python3.5

import utils
from client import OpenstackClient
from utils import Token


def check_status_service(session):
    """Lấy thông tin các agents của từng service 
    
    Arguments:
        session {[object]} -- [session trong openstack]
    
    Returns:
        [type] -- [dict]
    """

    token = Token()
    client = OpenstackClient(session_auth=token.session_auth)
    cinder_services = client.cinder_api.services.list()
    neutron_services = client.neutron_api.list_agents()
    nova_services = client.nova_api.services.list()
    return cinder_services, nova_services, neutron_services

def check_services_nova(services):
    """
    In ra màn hình theo from của plugin checkMK
    """

    print('<<<check_nova_info>>>')
    for service in services:
        print('service {0} of {1} : {2}'.format(service.binary,
                                                service.host,
                                                service.state))

def check_services_neutron(services):
    """
    In ra màn hình theo from của plugin checkMK
    """
    
    print('<<<check_neutron_info>>>')
    for service in services["agents"]:
        print('service {0} of {1} : {2}'.format(service['binary'],
                                                service['host'],
                                                service['alive']))
        
def check_services_cinder(services):
    """
    In ra màn hình theo from của plugin checkMK
    """

    print('<<<check_cinder_info>>>')
    for service in services:
        print('service {} of {} : {}'.format(service.binary,
                                             service.host,
                                             service.state))

def main():
    sess = utils.create_session_from_usename()
    data = check_status_service(session=sess)
    check_services_cinder(services=data[0])
    check_services_nova(services=data[1])
    check_services_neutron(services=data[2])

if __name__ == '__main__':
    main()
    