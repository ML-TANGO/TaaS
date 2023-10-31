import enum
import json
from typing import Optional

from sqlalchemy import Column
from sqlmodel import Column, Field, JSON, SQLModel


class ServiceStatus(enum.Enum):
    STARTED = "started"
    PREPARING = "preparing"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


RunningServiceStatuses = [
    ServiceStatus.STARTED,
    ServiceStatus.PREPARING,
    ServiceStatus.RUNNING,
]


StoppedServiceStatuses = [
    ServiceStatus.STOPPED,
    ServiceStatus.FAILED,
]


class ServiceBase(SQLModel):
    pass


class Service(ServiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: ServiceStatus = Field(default=ServiceStatus.STARTED, index=True)
    #: Additional informaiton specific to the deploy target.
    target_info: Optional[dict] = Field(default=None, sa_column=Column(JSON))


class ServiceRead(ServiceBase):
    status: ServiceStatus


class ServiceRequestParams(ServiceBase):
    pass
