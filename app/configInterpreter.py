import os
import json
from datetime import datetime, timezone
import graphviz
import natsort



def datetimestamputc():
    # Get the current UTC time
    now = datetime.now(timezone.utc)

    # Convert the UTC time to a human-readable format
    utc_timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    return utc_timestamp

def read_json_files():
    # Lets create nodes
    folder_path = '../tests'
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    # Create a dictionary to store the JSON data
    json_data = {}

    #json_files = ['starlab.json']

    # Iterate through the JSON files and convert them to dictionaries
    for file in json_files:
        with open(os.path.join(folder_path, file)) as json_file:
            data = json.load(json_file)
            json_data[file] = data

    return json_data

def get_connections(json_configs):
    c = {}
    connections = json_configs["connections"]
    for connection in connections:
        l = []
        fname_list = []
        connection_name = connection["name"]
        endpoints = connection["endpoints"]
        functions = connection["functions"]
        for f in functions:
            fname_list.append(f["choice"])

        fname_str = "::".join(fname_list)

        # Prints details of endpoints
        for endpoint in endpoints:
            choice_details_key = endpoint["choice"]
        
            if choice_details_key == "front_panel":
                l.append(endpoint[choice_details_key]["port_name"])
        l.append(fname_str)
        c[connection_name] = l
    return c

def get_front_panel_ports(json_configs):
    d = {}
    front_panel_ports = json_configs["front_panel_ports"]
    for fpp in front_panel_ports:
        fp_name = fpp["name"]
        if fpp["choice"] == "port_group":
            ports = fpp[fpp["choice"]]["ports"]
            for p in ports:
                port_number = p['front_panel_port']
                layer_1_profile_name = p['layer_1_profile_name']
                d[str(port_number)] = {"port_name": str(fp_name), 
                                "layer_1_profile_name": layer_1_profile_name}

        if fpp["choice"] == "front_panel_port":
                port_number  = fpp[fpp["choice"]]["front_panel_port"]
                layer_1_profile_name = fpp[fpp["choice"]]['layer_1_profile_name']
                d[str(port_number)] = {"port_name": str(fp_name), 
                                "layer_1_profile_name": layer_1_profile_name}
    return d
        

def create_vizualization(json_configs_dict=None, runtime_json_config=None):

    def get_uhd_port(endpoint):
        a = []
        for key, val in uhd_ports.items():
            if val['port_name'] == endpoint:
                # Encompasses when multiple ports in a port group
                a.append(key)
        return a

    # To be used when retrieving live configuration
    if runtime_json_config:
        json_configs_dict = {}
        json_configs_dict["runtimejson"] = runtime_json_config


    for json_test_name, json_configs in json_configs_dict.items():
        print(json_test_name, json_configs)
        ps = graphviz.Digraph('json_test_name')
        label_str = f"UHD Topology (Fetched @ {datetimestamputc()} ) "
        ps.attr(ffontname="Helvetica,Arial,sans-serif", 
                rankdir="TB", label=label_str, 
                ranksep='8', ordering="out")
        connections = get_connections(json_configs)
        uhd_ports= get_front_panel_ports(json_configs)
        with ps.subgraph(name='cluster_UHD') as c:
                c.attr(color="blue", label="UHDConnect", fontname="Helvetica,Arial,sans-serif")
                port_list_str = list(uhd_ports.keys())
                sorted_list = natsort.natsorted(port_list_str)
                for port in sorted_list:
                    c.node(port, shape="note", color='black', fontname="Helvetica,Arial,sans-serif")

        with ps.subgraph(name='cluster_Endpoints') as c:
                c.attr(color="green", area="200", label="Endpoints", fontname="Helvetica,Arial,sans-serif")
                used_uhd_p = []
                for connection_name, endpoints in connections.items():
                    c.node(endpoints[0], shape="note", color='black')
                    c.node(endpoints[1], shape="note", color='black')
                    # When not UHD connections, just endpoint to endpoint direct connection
                    if "bypass" in connection_name.lower(): 
                        pass
                        #ps.edge(endpoints[0], endpoints[1], dir="both")
                    else:
                        ep0_p = get_uhd_port(endpoints[0])
                        ep1_p = get_uhd_port(endpoints[1])
                        for ep_0_item in ep0_p:
                            if ep_0_item not in used_uhd_p:
                                used_uhd_p.append(ep_0_item)
                                ps.edge(endpoints[0], ep_0_item, dir="both", arrowsize='2', label=endpoints[2], labelfontcolor="turquoise")

        
                        for ep_1_item in ep1_p:
                            if ep_1_item not in used_uhd_p:
                                used_uhd_p.append(ep_1_item)
                                ps.edge(endpoints[1], ep_1_item, dir="both", arrowsize='2', label=endpoints[2], labelfontcolor="turquoise")
        ps.render(json_test_name, format='jpg', cleanup=True)
        
if __name__ == "__main__":
    json_configs_dict = read_json_files()
    create_vizualization(json_configs_dict=json_configs_dict, runtime_json_config=None)

    