from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
from app_services.UsersResource.user_service import UserResource
from app_services.GroupsResource.group_service import GroupResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Initiate flask application
application = Flask(__name__)
CORS(application)


@application.route('/')
def hello_world():
    """
    This method is for the "/" route (ex. http://localhost/),
    which just returns the string "Hello World!"
    """
    return '<u>Hello World!</u>'


@application.route('/users', methods=["GET", "POST"])
def get_users():
    """
    This method accesses the '/users' route, which supports
    GET and POST requests
    """

    if request.method == "GET":
        # GET Request - Get all users in the Users database

        # Call get_by_template with empty template
        res = UserResource.get_by_template({})

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "POST":
        # POST Request - Add a user to the Users database

        # Get the column-value dictionary
        data_dict = request.get_json()

        # Call insert_by_template
        res = UserResource.insert_by_template(data_dict)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


@application.route('/users/<user_id>', methods=["GET", "PUT", "DELETE"])
def get_by_user_id(user_id):
    """
    This method accesses the '/users/<user_id>' route,
    where user_id is any username in the Users database.
    This method supports GET, PUT, and DELETE requests.
    """

    if request.method == "GET":
        # GET Request - get the user with specified username
        # from the Users database

        # Call get_by_id to get the user's information
        res = UserResource.get_by_id(user_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "PUT":
        # PUT Request - Update a user's information

        # Get column-value pairs for the updated information
        data_dict = request.get_json()

        # Call update_by_id to update user's information
        res = UserResource.update_by_id(data_dict, user_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "DELETE":
        # DELETE Request - delete a user from the database

        # Call delete_by_id to delete user
        res = UserResource.delete_by_id(user_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


@application.route('/users/<user_id>/groups', methods=["GET", "POST"])
def get_groups_of_user(user_id):
    """
    This method accesses the '/users/<user_id>/groups' route,
    where user_id is any username in the Users database.
    This method supports GET and POST requests.
    """

    if request.method == "GET":
        # GET Request - Get list of all the groups the user
        # belongs to

        # Call get_groups to get the groups the user is in
        res = UserResource.get_groups(user_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "POST":
        # POST Request - add a user to a group

        # Get the group_id to add the user to
        data_dict = request.get_json()

        # Call add_user_to_group() to add the user to the group
        res = UserResource.add_user_to_group(data_dict, user_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    else:
        error_msg = "ERROR. Unsupported Operation"
        # Create response
        rsp = Response(json.dumps(error_msg, default=str),
                       status=404,
                       content_type="application/json")
        return rsp


@application.route('/groups', methods=["GET", "POST"])
def get_groups():
    """
    This method accesses the '/groups' route.
    This method supports GET and POST requests.
    """
    if request.method == "GET":
        # GET Request - get a list of all the groups in
        # the Groups database

        # Call get_by_template with empty dictionary
        # to get list of all groups
        res = GroupResource.get_by_template({})

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "POST":
        # POST Request - Add a group to the Groups database

        # Get the group_id and group_name from the request
        # body
        data_dict = request.get_json()

        # Call insert_by_template to insert new group into
        # Groups database
        res = GroupResource.insert_by_template(data_dict)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


@application.route('/groups/<group_id>', methods=["GET", "PUT", "DELETE"])
def get_by_group_id(group_id):
    """
    This method accesses the '/groups/<group_id>' route,
    where group_id is any group_id in the Groups database.
    This method supports GET, PUT, and DELETE requests.
    """

    group_id = int(group_id)
    if request.method == "GET":
        # GET Request - get information of the group
        # specified by the group_id

        # Call get_by_id to get information about
        # the group with specified group_id
        res = GroupResource.get_by_id(group_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "PUT":
        # PUT Request - update a group's information

        # Get column-value pairs for new information
        data_dict = request.get_json()

        # Call update_by_id to update the group's information
        res = GroupResource.update_by_id(data_dict, group_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "DELETE":
        # DELETE Request - delete the group specified
        # by the group_id

        # Call delete_by_id to delete the group
        res = GroupResource.delete_by_id(group_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    else:
        error_msg = "ERROR. Unsupported Operation"
        # Create response
        rsp = Response(json.dumps(error_msg, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


@application.route('/groups/<group_id>/users',
                   methods=["GET", "POST", "DELETE"])
def get_users_in_group(group_id):
    """
    This method accesses the '/groups/<group_id>/users' route,
    where group_id is any group_id in the Groups database.
    This method supports GET, POST, and DELETE requests.
    """
    if request.method == "GET":
        # GET Request - Get list of all users that belong to
        # the group specified by group_id

        # Call get_users to get all the users belonging to
        # the specified group
        res = GroupResource.get_users(group_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "POST":
        # POST Request - Add a user to a group

        # Get username from request body
        data_dict = request.get_json()

        # Call add_user_to_group to add the user to the group
        res = GroupResource.add_user_to_group(data_dict, group_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp

    elif request.method == "DELETE":
        # DELETE Request - delete a user from a group

        # Get username of user to delete
        data_dict = request.get_json()

        # Call remove_user_from_group to delete the user from the group
        res = GroupResource.remove_user_from_group(data_dict, group_id)

        # Create response
        rsp = Response(json.dumps(res, default=str),
                       status=200,
                       content_type="application/json")
        return rsp
    else:
        error_msg = "ERROR. Unsupported Operation"
        # Create response
        rsp = Response(json.dumps(error_msg, default=str),
                       status=200,
                       content_type="application/json")
        return rsp


if __name__ == '__main__':
    application.run()
