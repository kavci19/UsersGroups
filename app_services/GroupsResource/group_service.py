from app_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as DBService


class GroupResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        """
        This method gets all rows from the Groups table that
        match the template
        :param template: dictionary containing the column-value pairs
                         to match
        :return: all rows in the Groups table that match the template
        """
        success, res = DBService.find_by_template("UsersGroups",
                                                  "Groups", template)
        return success, res

    @classmethod
    def insert_by_template(cls, template):
        """
        This method inserts a group into the Groups table that
        match the template
        :param template: dictionary containing the column-value pairs
                         for the record to be inserted
        """
        success, res = DBService.insert_group_by_template("UsersGroups",
                                                          "Groups",
                                                          "group_id", template)
        return success, res

    @classmethod
    def delete_by_id(cls, group_id):
        """
        This method deletes the group that has the specified group_id

        :param group_id: the group_id of the group to delete from the
                             Groups table
        """

        # First delete all users from the group, in BelongsTo table
        DBService.delete_by_id("UsersGroups", "BelongsTo",
                               "group_id", group_id)

        # Next, delete the group in the Groups table
        res = DBService.delete_by_id("UsersGroups", "Groups",
                                     "group_id", group_id)
        return res

    @classmethod
    def get_by_id(cls, group_id):
        """
        This method gets the information of the group with the specified group_id
        :param group_id: the group_id of the group to get information about
        :return: the row in the Groups table that matches the group_id
        """

        group_id = int(group_id)

        res = DBService.get_by_id("UsersGroups", "Groups",
                                  "group_id", group_id)
        return res

    @classmethod
    def update_by_id(cls, template, group_id):
        """
        This method updates the group information of the group
        specified by the group_id
        :param template: dictionary containing the column-value pairs
                         of the new information
        :param group_id: the group_id of the group to update
        """

        res = DBService.update_by_id('UsersGroups', 'Groups',
                                     template, 'group_id', group_id)
        return res

    @classmethod
    def get_users(cls, group_id):
        """
        This method gets a list of all the users that belong to the
        group specified by the group_id
        :param group_id: the group_id of the group to get all the users of
        :return: links to all the users in the specified group
        """

        # Call get_users to get all users in the group
        res = DBService.get_users_in_group(group_id)

        # Call get_links to get links for each user in
        # the group
        res = cls.get_links(res, group_id)

        return res

    @classmethod
    def add_user_to_group(cls, template, group_id):
        """
        This method adds a user to the specified group
        :param template: dictionary containing the username of
                         the user to add to the group
        :param group_id: the group id of the group to add to
        """

        # Get the username of the user to add
        username = template["username"]

        # Call add_user_to_group() to add the user to the group
        res = DBService.add_user_to_group('UsersGroups', 'BelongsTo',
                                          group_id, username)
        return res

    @classmethod
    def remove_user_from_group(cls, template, group_id):
        """
        This method removes the specified user from the specified group
        :param template: dictionary containing the username of the
                         user to delete
        :param group_id: the group id of the group to delete from
        """

        # Get the username
        username = template["username"]

        # Call remove_user_from_group to remove the user from the group
        res = DBService.remove_user_from_group("UsersGroups", "BelongsTo",
                                               group_id, username)
        return res

    @classmethod
    def get_links(cls, usernames_and_emails, group_id):
        """
        This method inserts a list of links for each user that includes
        a link to the group, a link to the user, and the user's email

        :param usernames_and_emails: list of dictionaries, each dictionary
                                     containing username and email for a user

        :param group_id: The group id of the group that all the users belong to
        :return: The list of dictionaries, with the links added
        """

        # Go through each user's dictionary
        for r in usernames_and_emails:

            # Create a list of links
            links = []

            # Get the username of the user
            username = r['username']

            # Get the user's gmail
            email = r['gmail']

            # Create href to the group
            self_link = {'rel': 'self', 'href': f'/groups/{group_id}'}

            # Create href to the user's own "profile"
            user_link = {'ref': 'username', 'href': f'/users/{username}'}

            # Create href to user's email
            email_link = {'ref': 'email', 'href': f'{email}'}

            # Add links to list of links
            links.append(self_link)
            links.append(user_link)
            links.append(email_link)

            # Insert list of links into the user's dictionary
            r['links'] = links

        # Return updated dictionary list
        return usernames_and_emails
