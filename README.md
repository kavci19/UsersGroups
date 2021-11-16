Include in your repository any configuration files needed to build, run and test your codebase.

Write a README.md that describes in simple terms how to build, run and test your initial service. 


Configuration files:
    1. requirements.txt
    
        pip install -r requirements.txt

How to Build:
    1. Go into UsersGroups directory and install all necessary packages

        pip install -r requirements.txt

    2. Go into UsersGroups directory and run application.py
    3. Once running, you can open Postman on desktop and access the operational entrypoints listed below.
    
        Ex. http://127.0.0.1:5000/users


Unit Test Files:
    UsersGroups/app_services/GroupsResource/test_group_service.py
    UsersGroups/app_services/UsersResource/test_user_service.py
    
To run unit tests:
  1. For test_group_service.py
     
     1a. Navigate to 'UsersGroups/app_services/GroupsResource/'
     1b. Then run:
                    python -m unittest
  
  2. For test_user_service.py
     
     2a. Navigate to 'UsersGroups/app_services/UsersResource/'
     2b. Then run:
                    python -m unittest
  


The following entry points are operational:

Entry point: '/users'
Methods: "GET", "POST"
    GET: Get all users in the Users database
    POST: Add a user to the Users database



Entry point: '/users/<user_id>'
Methods: "GET", "PUT", "DELETE"
    GET: Get the user with specified username from the Users database
    PUT: Update a user's information
    DELETE: Delete a user from the Users database



Entry point: '/users/<user_id>/groups'
Methods: "GET", "POST"
    GET: Get list of all the groups the user belongs to
    POST: Add a user to a group



Entry point: '/groups'
Methods: "GET", "POST"
    GET: Get a list of all the groups in the Groups database
    POST: Add a group to the Groups database



Entry point: '/groups/<group_id>'
Methods: "GET", "PUT", "DELETE"
    GET: Get information of the group specified by the group_id
    PUT: Update a group's information
    DELETE: Delete the group specified by the group_id from
            the Groups database



Entry point: '/groups/<group_id>/users'
Methods: "GET", "POST", "DELETE"
    GET: Get list of all users that belong to the group specified by group_id
    POST: Add a user to a group
    DELETE: Delete a user from a group
