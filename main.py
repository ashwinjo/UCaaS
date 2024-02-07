import requests
import json
from flask import Flask
from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)

@app.route("/setUHDConfig/<uhdIP>", methods=['PUT'])
def set_uhd_config(uhdIP):
    url = f"http://{uhdIP}:80/connect/api/v1/config"

    payload = json.dumps({
    "profiles": {
        "layer_1_profiles": [
        {
            "name": "autoneg",
            "link_speed": "speed_100_gbps",
            "choice": "autonegotiation"
        }
        ]
    },
    "front_panel_ports": [
        {
        "name": "ixload_port_group_1",
        "choice": "port_group",
        "port_group": {
            "ingress_distribution": "copy",
            "ports": [
            {
                "front_panel_port": 9,
                "layer_1_profile_name": "autoneg"
            }
            ]
        }
        },
        {
        "name": "ixload_port_group_2",
        "choice": "port_group",
        "port_group": {
            "ingress_distribution": "copy",
            "ports": [
            {
                "front_panel_port": 10,
                "layer_1_profile_name": "autoneg"
            }
            ]
        }
        },
        {
        "name": "dpu_port_1",
        "choice": "port_group",
        "port_group": {
            "ingress_distribution": "copy",
            "ports": [
            {
                "front_panel_port": 5,
                "layer_1_profile_name": "autoneg"
            }
            ]
        }
        },
        {
        "name": "dpu_port_2",
        "choice": "port_group",
        "port_group": {
            "ingress_distribution": "copy",
            "ports": [
            {
                "front_panel_port": 6,
                "layer_1_profile_name": "autoneg"
            }
            ]
        }
        }
    ],
    "connections": [
        {
        "name": "ARP Bypass 1",
        "functions": [
            {
            "choice": "connect_arp",
            "connect_arp": {}
            }
        ],
        "endpoints": [
            {
            "choice": "front_panel",
            "front_panel": {
                "port_name": "ixload_port_group_1",
                "vlan": {
                "choice": "vlan_range",
                "vlan_range": {
                    "start": 1,
                    "count": 1
                }
                }
            }
            },
            {
            "choice": "front_panel",
            "front_panel": {
                "port_name": "ixload_port_group_2",
                "vlan": {
                "choice": "vlan_range",
                "vlan_range": {
                    "start": 1001,
                    "count": 1
                }
                }
            }
            }
        ]
        },
        {
        "name": "IxLoad VLAN to DUT PASSTHRU 1",
        "functions": [
            {
            "choice": "connect_ip",
            "connect_ip": {}
            }
        ],
        "endpoints": [
            {
            "choice": "front_panel",
            "front_panel": {
                "port_name": "ixload_port_group_1",
                "vlan": {
                "choice": "vlan_range",
                "vlan_range": {
                    "start": 1,
                    "count": 1
                }
                }
            }
            },
            {
            "choice": "front_panel",
            "front_panel": {
                "port_name": "dpu_port_1",
                "vlan": {
                "choice": "non_vlan"
                }
            }
            }
        ]
        },
        {
        "name": "IxLoad VLAN to DUT PASSTHRU 2",
        "functions": [
            {
            "choice": "connect_ip",
            "connect_ip": {}
            }
        ],
        "endpoints": [
            {
            "choice": "front_panel",
            "front_panel": {
                "port_name": "ixload_port_group_2",
                "vlan": {
                "choice": "vlan_range",
                "vlan_range": {
                    "start": 1001,
                    "count": 1
                }
                }
            }
            },
            {
            "choice": "front_panel",
            "front_panel": {
                "port_name": "dpu_port_2",
                "vlan": {
                "choice": "non_vlan"
                }
            }
            }
        ]
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
    return jsonify({"message": "Configuration has been set", "status_code":response.status_code})


@app.route("/getUHDConfig/<uhdIP>")
def get_uhd_config(uhdIP):
    url = f"http://{uhdIP}:80/connect/api/v1/config"
    headers = {
                'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data={}, verify=False)
    return jsonify({"message": "Configuration has been set", "status_code":response.status_code, "configuration": response.json()})


@app.route("/getUHDmetrics/<uhdIP>")
def get_uhd_metrics(uhdIP):
    url = f"http://{uhdIP}:80/connect/api/v1/metrics/operations/query"
    try:
        a = {
            "port_metrics":{}
        }
        response = requests.post(url, data=a,headers={"Content-type": "application/json"}, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # return the response content (data)
            return jsonify(response.json())
        else:
            return(f"Request failed with status code: {response.status_code}")

    except requests.RequestException as e:
        return(f"Request failed: {e}")


@app.route("/clearUHDmetrics/<uhdIP>")
def clear_uhd_metrics(uhdIP):
    url = f"http://{uhdIP}:80/connect/api/v1/metrics/operations/clear"

    payload = {}
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, params=payload, verify=False)
    return jsonify({"message": "Configuration has been cleared", "status_code":response.status_code})
   


if __name__ == "__main__":
    app.run(debug=True)


