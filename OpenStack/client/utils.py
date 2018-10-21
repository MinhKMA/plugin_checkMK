from keystoneauth1.identity import v3
from keystoneauth1 import session

import configparser
import json

def ini_file_loader():
    """ Load configuration from ini file"""

    parser = configparser.SafeConfigParser()
    parser.read('config.cfg')
    config_dict = {}

    for section in parser.sections():
        for key, value in parser.items(section, True):
            config_dict['%s-%s' % (section, key)] = value
    return config_dict

def create_session_from_usename(username=None, password=None,
                                project_domain_name=None,
                                project_name=None,
                                user_domain_name=None,
                                auth_url=None):
    """ get session authentication"""
    config_dict = ini_file_loader()
    username = username or config_dict['controller-username']
    password = password or config_dict['controller-password']
    project_domain_name = project_domain_name or config_dict['controller-project_domain_name']
    project_name = project_name or config_dict['controller-project_name']
    user_domain_name = user_domain_name or config_dict['controller-user_domain_name']
    auth_url = auth_url or config_dict['controller-auth_url']
    auth = v3.Password(auth_url=auth_url,
                       user_domain_name=user_domain_name,
                       username=username, password=password,
                       project_domain_name=project_domain_name,
                       project_name=project_name)
    sess = session.Session(auth=auth)
    return sess

def create_session_from_token(auth_url, token):
    """create session openstack from token
    
    Arguments:
        auth_url {[type: str]} -- [url identity openstack]
        token {[type: str]} -- [token openstack]
    
    Returns:
        [type:object] -- [session openstack]
    """

    auth = v3.token(auth_url=auth_url, token=token)
    sess = session.Session(auth=auth)
    return sess


class Token(object):
    """
    Lớp tạo session auth keystone phục vụ cho các thư viện openstack khác
    """
    session_auth = None
    def __init__(self,):
        """Khởi tạo phiên
        :params:
        - auth_ref = Lớp chung, đối tượng truyền vào chính là AuthPassword và AuthToken.
        :notes:
        - Sử dụng tính chất đa hình Python OOP
        - Mục đích khởi tạo ra kết nối tới openstack (keystone session)
        """
        self.config_dict = ini_file_loader()  
        self.session_auth = v3.Password(
            auth_url=self.config_dict['controller-auth_url'],
            username=self.config_dict['controller-username'],
            password=self.config_dict['controller-password'],
            project_id=self.config_dict['controller-project_id'],
            project_domain_name=self.config_dict['controller-project_domain_name'],
            user_domain_name=self.config_dict['controller-user_domain_name']
        )

