factory_settings['check_neutron_info_default_value'] = {
    'config': ((None, None), False),
}

def inventory_check_neutron_info(info):
    for line in info:
        line = " ".join(line)
        line = str(line)
        data = line.split(':')
        check_neutron_item = 'neutron services: ' + str(data[0])
        yield (check_neutron_item, "check_neutron_info_default_value")

def check_neutron_info(item, params, info):
    hostinfo_in_item=''
    state = None
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
    #print([(hostinfo_in_item, info_as_dict[hostinfo_in_item])])
    if info_as_dict[hostinfo_in_item] in ' True ':
        state = 0
    else:
        state = 2
    return state, "{}:{}".format(hostinfo_in_item, info_as_dict[hostinfo_in_item]), [(hostinfo_in_item, None)]

check_info ["check_neutron_info"] = {
    'default_levels_variable': "check_neutron_info_default_value",
    'inventory_function': inventory_check_neutron_info,
    'check_function': check_neutron_info,
    'service_description': 'neutron serivices info',
    'has_perfdata': True,
    'group': "check_mk_info",
}
