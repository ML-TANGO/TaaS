from abc import ABC, abstractmethod


class DeployTarget(ABC):
    def __init__(self, user_id: str, project_id: str):
        pass

    @abstractmethod
    def deploy(self, kubernetes_config: str):
        pass

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def status(self):
        pass

