import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi.responses import FileResponse
from app.configInterpreter import create_vizualization

app = FastAPI(title='UaaS',
              description='API Library to interact with UHDConnect')

# # Allowing CORS for all domains
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.post("/setUHDConfig/{uhdIP}/{req}")
async def set_uhd_config(uhdIP: str, req: str):
    url = f"http://{uhdIP}:80/connect/api/v1/config"
    json_d = json.loads(req)

    try:
        response = requests.post(url, json=json_d, verify=False)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        return {"message": "Configuration has been set", "status_code": response.status_code}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")


@app.get("/getUHDConfig/{uhdIP}")
def get_uhd_config(uhdIP: str):
    url = f"http://{uhdIP}:80/connect/api/v1/config"

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        return {"message": "Configuration fetched", "status_code": response.status_code, "configuration": response.json()}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")


@app.get("/getUHDmetrics/{uhdIP}")
def get_uhd_metrics(uhdIP: str):
    url = f"http://{uhdIP}:80/connect/api/v1/metrics/operations/query"
    try:
        """Need to make this customizable"""
        a = {"port_metrics":{}}
        response = requests.post(url, json=a, verify=False)

        # Check if the request was successful (status code 200)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")


@app.post("/clearUHDmetrics/{uhdIP}")
def clear_uhd_metrics(uhdIP: str):
    url = f"http://{uhdIP}:80/connect/api/v1/metrics/operations/clear"

    try:
        response = requests.post(url, verify=False)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        return {"message": "Metrics have been cleared", "status_code": response.status_code}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")



import os

# GET route to return the saved image
@app.get("/getUHDConfigAsImage/{uhdIP}")
async def show_image(uhdIP: str):
    try:
        create_vizualization(runtime_json_config=get_uhd_config(uhdIP)["configuration"])
        file_path = os.path.join("runtimejson.jpg")
        return FileResponse(file_path)
    except Exception as e:
        return {"error": str(e)}



# TODO: 
# 1. Files Cleaner
# 2. Port Metrics Graph generator