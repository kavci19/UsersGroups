from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class GroupResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template("UsersGroups", "Groups", template, None)
        return res

    @classmethod
    def insert_by_template(cls, template):
        res = d_service.insert_by_template("UsersGroups", "Groups", 'group_id', template)
        return res

    @classmethod
    def delete_by_id(cls, id):
        res = d_service.delete_by_id("UsersGroups", "Groups", "group_id", id)
        return res

    @classmethod
    def get_by_id(cls, id):
        res = d_service.get_by_id("UsersGroups", "Groups", "group_id", id)
        return res

    @classmethod
    def update_by_id(cls, template, id_no):
        res = d_service.update_by_id('UsersGroups', 'Groups', template, 'group_id', id_no)
        return res

    @classmethod
    def get_users(cls, group_id):
        res = d_service.get_users(group_id)
        res = cls.get_links(res, group_id)
        return res

    @classmethod
    def get_links(cls, usernames, group_id):
        for r in usernames:
            links = []
            username = r['username']
            self_link = {'rel': 'self', 'href': f'/groups/{group_id}'}
            user_link = {'ref': 'username', 'href': f'/users/{username}'}
            links.append(self_link)
            links.append(user_link)
            r['links'] = links
        return usernames