from flask import Flask, Response, request
import database_services.RDBService as d_service
from flask_cors import CORS
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.UsersResource.user_service import UserResource
from application_services.GroupsResource.group_service import GroupResource

application = Flask(__name__)
CORS(application)


@application.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@application.route('/users', methods=["GET", "POST"])
def get_users():
    if request.method == "GET":
        res = UserResource.get_by_template(request.args)
        # res = UserResource.get_links(res)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == "POST":
        res = UserResource.insert_by_template(request.form)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


@application.route('/users/<user_id>', methods = ["GET", "PUT", "DELETE"])
def get_by_user_id(user_id):
    if request.method == "GET":
        res = UserResource.get_by_id(user_id)
        # res = UserResource.get_links(res)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == "PUT":
        res = UserResource.update_by_id(request.form, user_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    else:
        res = UserResource.delete_by_id(user_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


@application.route('/users/<user_id>/groups', methods=["GET", "POST"])
def get_groups_of_user(user_id):
    if request.method == "GET":
        res = UserResource.get_groups(user_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    # elif request.method == "POST":
    #     res = UserResource.update_by_id(request.form, user_id)
    #     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    #     return rsp


@application.route('/groups', methods=["GET", "POST"])
def get_groups():
    if request.method == "GET":
        res = GroupResource.get_by_template(request.args)
        # res = GroupResource.get_links(res)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == "POST":
        res = UserResource.insert_by_template(request.form)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


@application.route('/groups/<group_id>', methods = ["GET", "PUT", "DELETE"])
def get_by_group_id(group_id):
    if request.method == "GET":
        res = GroupResource.get_by_id(group_id)
        # res = GroupResource.get_links(res)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == "PUT":
        res = UserResource.update_by_id(request.form, group_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    else:
        res = UserResource.delete_by_id(group_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


@application.route('/groups/<group_id>/users', methods = ["GET", "POST"])
def get_users_in_group(group_id):
    if request.method == "GET":
        res = GroupResource.get_users(group_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    # elif request.method == "POST":
    #     res = UserResource.update_by_id(request.form, group_id)
    #     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    #     return rsp
    # else:
    #     # ERROR


if __name__ == '__main__':
    application.run()
