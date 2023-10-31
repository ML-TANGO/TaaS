from fastapi import FastAPI, HTTPException

from targets.abc import DeployTarget


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def get_kubernetes_config():
    with open("kubernetes.yml", "r") as file:
        kubernetes_config = file.read()
    return kubernetes_config


def get_deploy_target(target_system: str) -> DeployTarget:
    if target_system == "local":
        from targets.local.docker import LocalDeploy
        return LocalDeploy()
    elif target_system == "gcp-gke":
        from targets.gcp.gke import GKEDeploy
        return GKEDeploy()
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported target system: {target_system}")


@app.on_event("startup")
def on_startup():
    pass


@app.get("/")
async def status():
    return Response(content="", status_code=200, media_type="text/plain")


@app.post("/deploy/{target_system}")
async def deploy(target_system: str):
    kubernetes_config = get_kubernetes_config()
    deploy_target: DeployTarget

    if target_system == "local":
        deploy_target = LocalDeploy()
    elif target_system == "gcp":
        deploy_target = GCPDeploy()
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported target system: {target_system}")

    try:
        deploy_target.deploy(kubernetes_config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Deployment to {target_system} succeeded"}



@app.post("/destroy/{target_system}")
async def destroy(target_system: str):
    deploy_target = get_deploy_target(target_system)
    try:
        deploy_target.destroy()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": f"Destruction of {target_system} succeeded"}



@app.get("/status/{target_system}")
async def status(target_system: str):
    deploy_target = get_deploy_target(target_system)
    try:
        deploy_target.status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": f"Status check on {target_system} succeeded"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

