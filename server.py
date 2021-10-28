import os
import subprocess
from ipaddress import ip_address
from ipaddress import ip_network

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from loguru import logger
from pydantic import BaseModel
from starlette import status

app = FastAPI()

github_nets = [
    "192.30.252.0/22",
    "185.199.108.0/22",
    "140.82.112.0/20",
    "143.55.64.0/20",
]


def validate_ip(addr: str) -> bool:
    ip = ip_address(addr)
    for net in github_nets:
        if ip in ip_network(net):
            return True
    return False


def execute_script(script_name: str) -> None:
    script_path = f"./scripts/{script_name}.sh"
    if not os.path.exists(script_path):
        logger.info(f"{script_name} doesn't exist")
        return
    logger.info("Executing logs:")
    subprocess.call(script_path)


class PayloadScheme(BaseModel):
    class Repository(BaseModel):
        name: str

    ref: str
    repository: Repository


@app.post("/payload")
async def receive_webhook(request: Request, data: PayloadScheme):
    ip = request.client.host
    logger.info(f"New request from {ip}")
    if not validate_ip(ip):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Go Away")

    branch_name = data.ref.split("/")[-1]
    script_name = f"{data.repository.name}-{branch_name}"
    logger.info(f"Executing {script_name}")
    execute_script(script_name)
