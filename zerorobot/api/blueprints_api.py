import json as JSON
import jsonschema
from jsonschema import Draft4Validator
from flask import Blueprint, jsonify, request

from zerorobot import blueprint
from zerorobot import service_collection as scol
from zerorobot import template_collection as tcol
from zerorobot.service_collection import ServiceConflictError

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

Blueprint_schema = JSON.load(open(dir_path + '/schema/Blueprint_schema.json'))
Blueprint_schema_resolver = jsonschema.RefResolver('file://' + dir_path + '/schema/', Blueprint_schema)
Blueprint_schema_validator = Draft4Validator(Blueprint_schema, resolver=Blueprint_schema_resolver)


blueprints_api = Blueprint('blueprints_api', __name__)


@blueprints_api.route('/blueprints', methods=['POST'])
def ExecuteBlueprint():
    '''
    Execute a blueprint on the ZeroRobot
    It is handler for POST /blueprints
    '''
    inputs = request.get_json()
    try:
        Blueprint_schema_validator.validate(inputs)
    except jsonschema.ValidationError as err:
        return JSON.dumps({'code': 400, 'message': str(err)}), 400, {"Content-type": 'application/json'}

    try:
        actions, services = blueprint.parse(inputs['content'])
    except blueprint.BadBlueprintFormatError as err:
        return JSON.dumps({'code': 400, 'message': str(err.args[1])}), 400, {"Content-type": 'application/json'}

    for service in services:
        srv = None
        try:
            srv = create_service(service['template'], service['service'], service['data'])
        except KeyError:
            return JSON.dumps({'code': 404, 'message': "template '%s' not found" % service['template']}), \
                404, {"Content-type": 'application/json'}
        except ServiceConflictError:
            # TODO: update service data
            # srv = scol.get_by_name(service['service'])
            pass

    for action in actions:
        try:
            schedule_action(action['service'], action['action'])
        except KeyError:
            return JSON.dumps({'code': 404, 'message': "service '%s' not found" % action['service']}), \
                404, {"Content-type": 'application/json'}

    return "", 204, {"Content-type": 'application/json'}


def create_service(template, name, data):
    TemplateClass = tcol.get(template)
    service = TemplateClass(name)
    scol.add(service)
    return service

def schedule_action(service, action):
    service = scol.get_by_name(service)
    service.schedule_action(action)