check_mk plugin 

- Trên server: Chú ý 2 file `check_mk_info` và `check_mk_info.py`

```
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
│   └── check_mk_info
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
        │   └── check_mk_info.py
        ├── sidebar
        ├── views
        ├── visuals
        └── wato
```

file `check_mk_info`

```
#!/usr/bin/python3.5


factory_settings['check_mk_info_default_value'] = {
    'config': ((None, None), False),
}


def inventory_check_mk_info(info):
    for line in info:
       check_mysql_info_item = ''
       line = " ".join(line)
       line = str(line)
       data = line.split(':')
       check_mysql_info_item =  "MySQL service: " + str(data[0])
       yield (check_mysql_info_item, "check_mk_info_default_value")


def check_mk_info(item, params, info):
    hostinfo_in_item=''
    if ":" in item:
        item_as_list = item.split(": ")
        host_in_item, hostinfo_in_item = item_as_list
    #print(host_in_item)
    #print(hostinfo_in_item)
    info_as_dict = {}
    for line in info:
        #print line
        line = " ".join(line)
        line = str(line)
        if ":" in line:
            line_as_list = line.split(':')
            info_as_dict.update({line_as_list[0]: line_as_list[1]})
    #print(info_as_dict[hostinfo_in_item])
    #print([(hostinfo_in_item, int(info_as_dict[hostinfo_in_item]))])
    return 0, "{} : {}".format(hostinfo_in_item, info_as_dict[hostinfo_in_item]), [(hostinfo_in_item, int(info_as_dict[hostinfo_in_item]))]

check_info ["check_mk_info"] = {
    'default_levels_variable': "check_mk_info_default_value",
    'inventory_function': inventory_check_mk_info,
    'check_function': check_mk_info,
    'service_description': 'CheckMK info',
    'has_perfdata': True,
    'group': "check_mk_info",
}
```

file `check_mk_info.py`

```
#!/usr/bin/python3.5


def perfometer_check_mk_info(row, check_command, perf_data):
    number = int(perf_data[0][1])
    color = "#00ff00"
    return number, perfometer_linear(100,color)

perfometers['check_mk-check_mk_info'] = perfometer_check_mk_info
```

- trên agent

```
[root@check_mk ~]# check_mk_agent | head
<<<check_mk>>>
Version: 1.5.0p5
AgentOS: linux
Hostname: check_mk
AgentDirectory: /etc/check_mk
DataDirectory: /var/lib/check_mk_agent
SpoolDirectory: /var/lib/check_mk_agent/spool
PluginsDirectory: /usr/lib/check_mk_agent/plugins
LocalDirectory: /usr/lib/check_mk_agent/local
<<<df>>>
[root@check_mk ~]# cd /usr/lib/check_mk_agent/plugins
[root@check_mk plugins]# ls
check_mk_info.py
[root@check_mk plugins]# ./check_mk_info.py 
<<<check_mk_info>>>
Number of insert per second : 1
Number of select per second : 0
Number of query per second : 1
[root@check_mk plugins]# 
[root@check_mk plugins]# cat check_mk_info.py 
#!/usr/bin/python3.5

import pymysql
import time

def last(connect):
    cur = connect.cursor()
    cur.execute("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS "
                "where VARIABLE_NAME = 'COM_SELECT' "
                "or VARIABLE_NAME = 'COM_INSERT' "
                "or VARIABLE_NAME = 'QUERIES';")
    result = cur.fetchall()
    select = int(result[0][0])
    insert = int(result[1][0])
    query = int(result[2][0])
    return select, insert, query


def calculator():
    conn = pymysql.connect(host='127.0.0.1',
                            user='root', passwd='minhkma',
                            db='information_schema')
    last_select, last_insert, last_query = last(conn)
    time.sleep(1)
    now_select, now_insert, now_query = last(conn)
    number_select = now_select - last_select
    number_insert = now_insert - last_insert
    number_query = now_query - last_query
    return number_select, number_insert, number_query


def main():
    number_select, number_insert, number_query = calculator()
    print('<<<check_mk_info>>>')
    print('Number of insert per second : {0}'.format(number_insert))
    print('Number of select per second : {0}'.format(number_select))
    print('Number of query per second : {0}'.format(number_query))


if __name__ == '__main__':
    main()
```
