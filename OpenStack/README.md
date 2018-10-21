# Giám sát trạng thái các services trong OpenStack thông qua check_MK

## Môi trường:

- CheckMK 1.5
- OpenStack Queens 
- Python3.5

    + Cách cài đặt python3.5

    ```
    yum -y install https://centos7.iuscommunity.org/ius-release.rpm
    yum -y install python35u
    yum -y install python35u-pip
    yum install python35u-devel -y
    pip3.5 install python-openstackclient
    pip3.5 install python-neutronclient
    ```

## Thực hiện trên phía client

- Trước tiên ta kiểm tra xem thực mục đặt plugin phia client 

    ```
    [root@check_mk plugins]# check_mk_agent | head
    <<<check_mk>>>
    Version: 1.5.0p5
    AgentOS: linux
    Hostname: check_mk
    AgentDirectory: /etc/check_mk
    DataDirectory: /var/lib/check_mk_agent
    SpoolDirectory: /var/lib/check_mk_agent/spool
    PluginsDirectory: /usr/lib/check_mk_agent/plugins
    LocalDirectory: /usr/lib/check_mk_agent/local
    ```

- Thư plugin check được đặt tại thư mục `/usr/lib/check_mk_agent/plugins`. Các bạn có thể tải scripts ở <a href="https://github.com/MinhKMA/plugin_checkMK/tree/master/OpenStack/client">Github</a> cá nhân của mình. 

    ```
    [root@check_mk plugins]# pwd
    /usr/lib/check_mk_agent/plugins
    [root@check_mk plugins]# ls
    check_nova.py  check_services.py  client.py  config.cfg  utils.py
    [root@check_mk plugins]# 
    ```

    + Trong file `config.cfg` khai báo thông tin xác thực với hệ thống OpenStack
    + Chấp quyền cho các scripts trong thư mục
    
    ```
    [root@check_mk plugins]# pwd
    /usr/lib/check_mk_agent/plugins
    [root@check_mk plugins]# chmod +x *
    ```

    + Kiểm tra lại script check 

    ```
    [root@check_mk plugins]# pwd
    /usr/lib/check_mk_agent/plugins
    [root@check_mk plugins]# ./check_services.py 
    <<<check_cinder_info>>>
    service cinder-backup of controller1 : down
    service cinder-scheduler of controller1 : up
    service cinder-volume of controller1@lvm : up
    <<<check_nova_info>>>
    service nova-conductor of controller1 : up
    service nova-consoleauth of controller1 : up
    service nova-scheduler of controller1 : up
    service nova-compute of compute1 : up
    service nova-compute of compute2 : up
    <<<check_neutron_info>>>
    service neutron-dhcp-agent of compute1 : True
    service neutron-linuxbridge-agent of controller1 : True
    service neutron-metadata-agent of compute1 : True
    service neutron-linuxbridge-agent of compute2 : True
    service neutron-metadata-agent of compute2 : True
    service neutron-linuxbridge-agent of compute1 : True
    service neutron-dhcp-agent of compute2 : True
    service neutron-l3-agent of controller1 : True
    ```

    + CheckMK quy định tên của plugin được đặt trong `<<<name_plugin>>>`

## Thực hiện trên server

- Truy cập vào site omd. Ở đây site OMD của mình là `monitoring`
   
   ```
   su - monitoring
   ```

- cd vào trong thư mục chứa các files cần đặt trên server:

    ```
    OMD[monitoring]:/opt/omd/sites/monitoring/local/share/check_mk$ 
    OMD[monitoring]:/opt/omd/sites/monitoring/local/share/check_mk$ tree
    .
    ├── agents
    │   ├── bakery
    │   ├── linux
    │   │   └── alert_handlers
    │   ├── plugins
    │   └── special
    ├── alert_handlers
    ├── checkman
    ├── checks
    │   ├── check_cinder_info
    │   ├── check_neutron_info
    │   └── check_nova_info
    ├── inventory
    ├── locale
    ├── mibs
    ├── notifications
    ├── pnp-rraconf
    ├── pnp-templates
    ├── reporting
    │   └── images
    └── web
        ├── htdocs
        │   └── images
        └── plugins
            ├── config
            ├── dashboard
            ├── icons
            ├── metrics
            ├── pages
            ├── perfometer
            ├── sidebar
            ├── views
            ├── visuals
            └── wato

    31 directories, 3 files
    OMD[monitoring]:/opt/omd/sites/monitoring/local/share/check_mk$ 
    ```

    + Ở đây có 2 thư mục : `~/checks/` và `~/web/plugins/perfometer/`
    + Ý nghĩa của 2 thư mục này:
        +  Đối với thư mục `checks`: Làm nhiệm vụ thu thập output từ script trên client để xử lý vào hiển thị lên wato trên dashboard checkMK
        + Đối với thư mục `/web/plugins/perfometer`: Lấy giá trị của mỗi metric hiển thị lên cột `PERF-O-METER` trên checkMK
        
            <img src='https://i.imgur.com/WLbT2eO.png'>

    + Tải các scripts từ <a href="https://github.com/MinhKMA/plugin_checkMK/tree/master/OpenStack/server">Github</a> đặt vào thư mục `checks` 

    ```
    OMD[monitoring]:/opt/omd/sites/monitoring/local/share/check_mk$ ls checks/
    check_cinder_info  check_neutron_info  check_nova_info
    OMD[monitoring]:/opt/omd/sites/monitoring/local/share/check_mk$ 
    ```
- Tiến hành debug trên server

    + Sử dụng 2 lệnh dưới đây để debug

    ```
    check_mk --checks=check_cinder_info -I server
    check_mk --debug -nv --checks=check_cinder_info server
    ```

    + Trong đó `check_cinder_info` là tên của plugin, `server` là tên của host client trong checkMK.

    ```
    OMD[monitoring]:/opt/omd/sites/monitoring/local/share/check_mk$ check_mk --debug -nv --checks=check_cinder_info server
    Check_MK version 1.5.0p5
    + FETCHING DATA
    [agent] Execute data source
    [piggyback] Execute data source
    cinder serivices info cinder services: service cinder-backup of controller1 CRIT - service cinder-backup of controller1 : down
    cinder serivices info cinder services: service cinder-scheduler of controller1 OK - service cinder-scheduler of controller1 : up
    cinder serivices info cinder services: service cinder-volume of controller1@lvm OK - service cinder-volume of controller1@lvm : up
    OK - [agent] Version: 1.5.0p5, OS: linux, execution time 2.7 sec | execution_time=2.742 user_time=0.020 system_time=0.000 children_user_time=0.000 children_system_time=0.000 cmk_time_agent=2.726
    ```
## Trên dashboard:

- Tiến hành discovery lại services

    <img src='https://i.imgur.com/IW5e7NA.png'>

- Chọn `Bulk discovery`

    <img src='https://i.imgur.com/kQZLzzu.png'>

- Chọn start sau đó save lại nhưng gì đã thay đổi 

    <img src='https://i.imgur.com/QaFyVSE.png'>

    <img src='https://i.imgur.com/C0Nq8KF.png'>
