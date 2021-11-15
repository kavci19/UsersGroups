import unittest
from user_service import UserResource


class Test_TestUserService(unittest.TestCase):

    # check if a user can be queried by a query string/template
    def test_get_by_template(self):
        template = {'first_name': 'Kaan'}
        success, res = UserResource.get_by_template(template)
        assert template.items() <= res[0].items()
        self.assertEqual(len(res), 1)
        self.assertTrue(success)

    # check if a new user can be successfully added to the database
    def test_insert_by_id(self):
        user = {'username': 'foo1234',
                'first_name': 'Foo',
                'last_name': 'Bar',
                'address': '508 W 114th St.',
                'city': 'New York',
                'state': 'New York',
                'country': 'USA',
                'gmail': 'foo123@columbia.edu',
                'phone_number': '123-456-7890'
                }
        success, res = UserResource.insert_by_template(user)
        self.assertEqual(success, True)
        success, res = UserResource.get_by_id('foo1234')
        assert user.items() <= res[0].items()
        self.assertEqual(len(res), 1)
        self.assertTrue(success)

    # check if a user can be successfully removed from the database
    def test_delete_by_id(self):
        username = 'foo1234'
        success, res = UserResource.delete_by_id(username)
        self.assertTrue(success)
        success, res = UserResource.get_by_id(username)
        self.assertEqual(len(res), 0)

    # check if a user can be queried by username
    def test_get_by_id(self):
        template = {'username': 'koa2107'}
        success, res = UserResource.get_by_id(template['username'])
        assert template.items() <= res[0].items()
        self.assertEqual(len(res), 1)
        self.assertTrue(success)

    # check if a user can have their information updated by id
    def test_update_by_id(self):
        username = 'koa2107'

        # get the user's old data
        success, res = UserResource.get_by_id(username)
        self.assertTrue(success)
        old_user_data = res[0]
        new_template = {'phone_number': '111-111-1111'}
        success, res = UserResource.update_by_id(new_template, username)
        self.assertTrue(success)

        # check that all the user's information is the same, except for a changed phone number
        success, res = UserResource.get_by_id(username)
        new_user_data = old_user_data
        new_user_data['phone_number'] = new_template['phone_number']
        self.assertEqual(new_user_data, res[0])

    # check if a user can be successfully added to a group
    def test_add_user_to_group(self):
        template = {'group_id': 4}
        username = 'koa2107'

        # add koa2107 to group 2
        success, res = UserResource.add_user_to_group(template, username)
        self.assertTrue(success)

        # check if koa2107 is now in group 2
        success, res = UserResource.get_groups(username)
        self.assertTrue(success)

        foundGroup = False
        for group in res:
            if group['group_id'] == template['group_id']:
                foundGroup = True
                break
        self.assertTrue(foundGroup)




if __name__ == '__main__':
    unittest.main()
