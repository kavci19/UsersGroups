from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class UserResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template("UsersAddresses", "Users",
                                       template, None)
        return res

    @classmethod
    def insert_by_template(cls, template):
        res = d_service.insert_by_template("UsersAddresses", "Users", 'userID', template)
        return res

    @classmethod
    def delete_by_id(cls, id):
        res = d_service.delete_by_id("UsersAddresses", "Users", "userID", id)
        return res

    @classmethod
    def get_by_id(cls, id):
        res = d_service.get_by_id("UsersAddresses", "Users", "userID", id)
        return res

    @classmethod
    def update_by_id(cls, template, id_no):
        res = d_service.update_by_id('UsersAddresses', 'Users', template, 'userID', id_no)
        return res

    @classmethod
    def get_links(self, resource_data):
        for r in resource_data:
            links = []
            user_id = r['userID']
            address_id = r['addressID']
            self_link = {'rel': 'self', 'href': f'/users{user_id}'}
            address_link  = {'ref': 'address', 'href': f'/addresses/{address_id}'}
            links.append(self_link)
            links.append(address_link)
            r['links'] = links
        return resource_data