from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
from application_services.UsersResource.user_service import UserResource
from application_services.GroupsResource.group_service import GroupResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


application = Flask(__name__)
CORS(application)


@application.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@application.route('/users', methods=["GET", "POST"])
def get_users():
    if request.method == "GET":
        res = UserResource.get_by_template(request.args)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "POST":
        data_dict = request.get_json()
        res = UserResource.insert_by_template(data_dict)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


@application.route('/users/<user_id>', methods=["GET", "PUT", "DELETE"])
def get_by_user_id(user_id):
    if request.method == "GET":
        res = UserResource.get_by_id(user_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "PUT":
        data_dict = request.get_json()
        res = UserResource.update_by_id(data_dict, user_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "DELETE":
        res = UserResource.delete_by_id(user_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


@application.route('/users/<user_id>/groups', methods=["GET", "POST"])
def get_groups_of_user(user_id):
    if request.method == "GET":
        res = UserResource.get_groups(user_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "POST":
        data_dict = request.get_json()
        res = UserResource.add_user_to_group(data_dict, user_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    else:
        error_msg = "ERROR. Unsupported Operation"
        rsp = Response(json.dumps(error_msg, default=str),
                       status=404,
                       content_type="application/json")
        return rsp


@application.route('/groups', methods=["GET", "POST"])
def get_groups():
    if request.method == "GET":
        res = GroupResource.get_by_template(request.args)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "POST":
        data_dict = request.get_json()
        res = GroupResource.insert_by_template(data_dict)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


@application.route('/groups/<group_id>', methods=["GET", "PUT", "DELETE"])
def get_by_group_id(group_id):
    group_id = int(group_id)
    if request.method == "GET":
        res = GroupResource.get_by_id(group_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "PUT":
        data_dict = request.get_json()
        res = GroupResource.update_by_id(data_dict, group_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "DELETE":
        res = GroupResource.delete_by_id(group_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    else:
        error_msg = "ERROR. Unsupported Operation"
        rsp = Response(json.dumps(error_msg, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


@application.route('/groups/<group_id>/users',
                   methods=["GET", "POST", "DELETE"])
def get_users_in_group(group_id):
    if request.method == "GET":
        res = GroupResource.get_users(group_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "POST":
        data_dict = request.get_json()
        res = GroupResource.add_user_to_group(data_dict, group_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    elif request.method == "DELETE":
        data_dict = request.get_json()
        res = GroupResource.remove_user_from_group(data_dict, group_id)
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    else:
        error_msg = "ERROR. Unsupported Operation"
        rsp = Response(json.dumps(error_msg, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


if __name__ == '__main__':
    application.run()
