# DO NOT EDIT THIS FILE. This file will be overwritten when re-running go-raml.

from .Action import Action
from .Blueprint import Blueprint
from .BlueprintResult import BlueprintResult
from .Eco import Eco
from .EnumRobotInfoType import EnumRobotInfoType
from .EnumServiceStateState import EnumServiceStateState
from .EnumTaskState import EnumTaskState
from .EnumWebHookKind import EnumWebHookKind
from .Error import Error
from .Logs import Logs
from .Metrics import Metrics
from .Metricscpu import Metricscpu
from .Metricsmemory import Metricsmemory
from .Repository import Repository
from .RobotInfo import RobotInfo
from .RobotInforepositories import RobotInforepositories
from .Service import Service
from .ServiceCreate import ServiceCreate
from .ServiceCreated import ServiceCreated
from .ServiceFilter import ServiceFilter
from .ServiceState import ServiceState
from .Task import Task
from .TaskCreate import TaskCreate
from .Template import Template
from .TemplateRepository import TemplateRepository
from .WebHook import WebHook

from .blueprints_service import BlueprintsService
from .robot_service import RobotService
from .services_service import ServicesService
from .templates_service import TemplatesService

from .passthrough_client_admin import PassThroughClientAdmin
from .passthrough_client_user import PassThroughClientUser
from .passthrough_client_service import PassThroughClientService
from .http_client import HTTPClient


class Client:
    def __init__(self, base_uri=""):
        http_client = HTTPClient(base_uri)
        self.security_schemes = Security(http_client)
        self.blueprints = BlueprintsService(http_client)
        self.robot = RobotService(http_client)
        self.services = ServicesService(http_client)
        self.templates = TemplatesService(http_client)
        self.close = http_client.close


class Security:
    def __init__(self, http_client):
        self.passthrough_client_admin = PassThroughClientAdmin(http_client)
        self.passthrough_client_user = PassThroughClientUser(http_client)
        self.passthrough_client_service = PassThroughClientService(http_client)
