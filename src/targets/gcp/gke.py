import subprocess

from targets.abc import DeployTarget


class GKEDeploy(DeployTarget):

    def deploy(self, kubernetes_config: str):
        with open("kubernetes.yml", "w") as file:
            file.write(kubernetes_config)
        deploy_command = ["gcloud", "container", "clusters", "get-credentials", "your-cluster", "--zone", "your-zone"]
        subprocess.run(deploy_command, check=True)
        apply_command = ["kubectl", "apply", "-f", "kubernetes.yml"]
        subprocess.run(apply_command, check=True)

    def destroy(self):
        destroy_command = ["kubectl", "delete", "-f", "kubernetes.yml"]
        subprocess.run(destroy_command, check=True)

    def status(self):
        status_command = ["kubectl", "get", "all"]
        subprocess.run(status_command, check=True)

