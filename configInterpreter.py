"""
"front_panel_ports": [
        {"name": "ixload_port_group_1",   "choice": "port_group","port_group":   {"ingress_distribution": "copy","ports": [{"front_panel_port":  9,  "layer_1_profile_name": "autoneg"}]}},
        {"name": "ixload_port_group_2",   "choice": "port_group","port_group":   {"ingress_distribution": "copy","ports": [{"front_panel_port": 10,  "layer_1_profile_name": "autoneg"}]}},
        {"name": "dpu_port_1",            "choice": "port_group","port_group":   {"ingress_distribution": "copy","ports": [{"front_panel_port": 5,   "layer_1_profile_name": "autoneg"}]}},
        {"name": "dpu_port_2",            "choice": "port_group","port_group":   {"ingress_distribution": "copy","ports": [{"front_panel_port": 6,   "layer_1_profile_name": "autoneg"}]}}
      ],
    "connections": [
      {
        "name": "ARP Bypass 1",
        "functions": [{"choice": "connect_arp","connect_arp": {}}],
        "endpoints": [
          {"choice": "front_panel","front_panel": {"port_name": "ixload_port_group_1","vlan": {"choice": "vlan_range","vlan_range":   {"start":    1,"count": 1}}}},
          {"choice": "front_panel","front_panel": {"port_name": "ixload_port_group_2","vlan": {"choice": "vlan_range","vlan_range":   {"start": 1001,"count": 1}}}}
        ]
      },
      {
        "name": "IxLoad VLAN to DUT PASSTHRU 1",
        "functions": [{"choice": "connect_ip","connect_ip": {}}],
        "endpoints": [
          {"choice": "front_panel","front_panel": {"port_name": "ixload_port_group_1","vlan": {"choice": "vlan_range","vlan_range":   {"start": 1,"count": 1}}}},
          {"choice": "front_panel","front_panel": {"port_name": "dpu_port_1","vlan": {"choice": "non_vlan"}}}
        ]
      },
      {
        "name": "IxLoad VLAN to DUT PASSTHRU 2",
        "functions": [{"choice": "connect_ip","connect_ip": {}}],
        "endpoints": [
          {"choice": "front_panel","front_panel": {"port_name": "ixload_port_group_2","vlan": {"choice": "vlan_range","vlan_range":   {"start": 1001,"count": 1}}}},
          {"choice": "front_panel","front_panel": {"port_name": "dpu_port_2","vlan": {"choice": "non_vlan"}}}
        ]
      }
    ]


"""


import graphviz

ps = graphviz.Digraph('pet-shop')
ps.attr(rankdir="LR")


# Lets create nodes

a = [
        {"name": "ixload_port_group_1",   "choice": "port_group","port_group":   {"ingress_distribution": "copy","ports": [{"front_panel_port":  9,  "layer_1_profile_name": "autoneg"}]}},
        {"name": "ixload_port_group_2",   "choice": "port_group","port_group":   {"ingress_distribution": "copy","ports": [{"front_panel_port": 10,  "layer_1_profile_name": "autoneg"}]}},
        {"name": "dpu_port_1",            "choice": "port_group","port_group":   {"ingress_distribution": "copy","ports": [{"front_panel_port": 5,   "layer_1_profile_name": "autoneg"}]}},
        {"name": "dpu_port_2",            "choice": "port_group","port_group":   {"ingress_distribution": "copy","ports": [{"front_panel_port": 6,   "layer_1_profile_name": "autoneg"}]}}
    ]




with ps.subgraph(name='cluster_Endpoints') as c:
    c.attr(color="blue", label="Endpoints")
    for item in a:
        ports_conn_name = item["name"]
        c.node(ports_conn_name, shape="square", color='blue')

with ps.subgraph(name='cluster_UHD') as c:
    c.attr(color="black",label="UHDConnect")
    for item in a:
        ports = item["port_group"]["ports"]
        for p in ports:
            port_name = str(p['front_panel_port'])
            c.node(port_name, shape="square", color='black')

for connections in a:  
    ports_conn_name = connections["name"] 
    portstr = ""
    ports = connections["port_group"]["ports"]
    print(ports)
    for p in ports:
        print()
        port = str(p['front_panel_port'])
        portstr +=port
        ps.edge(ports_conn_name, portstr)
    
print(ps.view())