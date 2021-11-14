from app_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as DBService


class GroupResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = DBService.find_by_template("UsersGroups", "Groups", template)
        return res

    @classmethod
    def insert_by_template(cls, template):
        res = DBService.insert_group_by_template("UsersGroups",
                                                 "Groups",
                                                 "group_id", template)
        return res

    @classmethod
    def delete_by_id(cls, id_to_delete):
        DBService.delete_by_id("UsersGroups", "BelongsTo",
                               "group_id", id_to_delete)

        res = DBService.delete_by_id("UsersGroups",
                                     "Groups", "group_id", id_to_delete)
        return res

    @classmethod
    def get_by_id(cls, id_to_get):
        res = DBService.get_by_id("UsersGroups", "Groups",
                                  "group_id", id_to_get)
        return res

    @classmethod
    def update_by_id(cls, template, id_no):
        res = DBService.update_by_id('UsersGroups', 'Groups',
                                     template, 'group_id', id_no)
        return res

    @classmethod
    def get_users(cls, group_id):
        res = DBService.get_users(group_id)
        res = cls.get_links(res, group_id)
        return res

    @classmethod
    def add_user_to_group(cls, template, group_id):
        username = template["username"]
        res = DBService.add_user_to_group('UsersGroups', 'BelongsTo',
                                          group_id, username)
        return res

    @classmethod
    def remove_user_from_group(cls, template, group_id):
        username = template["username"]
        res = DBService.remove_user_from_group("UsersGroups", "BelongsTo",
                                               group_id, username)
        return res

    @classmethod
    def get_links(cls, usernames_and_emails, group_id):
        for r in usernames_and_emails:
            links = []
            username = r['username']
            email = r['gmail']
            self_link = {'rel': 'self', 'href': f'/groups/{group_id}'}
            user_link = {'ref': 'username', 'href': f'/users/{username}'}
            email_link = {'ref': 'email', 'href': f'{email}'}
            links.append(self_link)
            links.append(user_link)
            links.append(email_link)
            r['links'] = links
        return usernames_and_emails
