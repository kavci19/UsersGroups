import sys
sys.path.append("../")
from BaseApplicationResource import BaseApplicationResource
sys.path.append("../../database_services")
import RDBService as DBService


class UserResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        success, res = DBService.find_by_template("UsersGroups",
                                                  "Users", template)
        return success, res

    @classmethod
    def insert_by_template(cls, template):
        success, res = DBService.insert_user_by_template("UsersGroups",
                                                         "Users",
                                                         "username",
                                                         template)
        return success, res

    @classmethod
    def delete_by_id(cls, id_to_delete):
        success, res = DBService.delete_by_id("UsersGroups", "Users",
                                              "username", id_to_delete)
        return success, res

    @classmethod
    def get_by_id(cls, id_to_get):
        success, res = DBService.get_by_id("UsersGroups", "Users",
                                           "username", id_to_get)
        return success, res

    @classmethod
    def update_by_id(cls, template, id_no):
        success, res = DBService.update_by_id("UsersGroups", "Users",
                                              template, "username", id_no)
        return success, res

    @classmethod
    def add_user_to_group(cls, template, username):
        group_id = template["group_id"]
        success, res = DBService.add_user_to_group("UsersGroups", "BelongsTo",
                                                   group_id, username)
        return success, res

    @classmethod
    def get_groups(cls, user_id):
        success, res = DBService.get_groups(user_id)
        res = cls.get_links(res, user_id)
        return success, res

    @classmethod
    def get_links(cls, group_ids, user_id):
        for r in group_ids:
            links = []
            group_id = r["group_id"]
            self_link = {'rel': 'self', 'href': f'/users/{user_id}'}
            group_link = {'ref': 'group_id', 'href': f'/groups/{group_id}'}
            links.append(self_link)
            links.append(group_link)
            r['links'] = links
        return group_ids
