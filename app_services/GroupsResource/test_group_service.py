import unittest
from group_service import GroupResource


class TestGroupResource(unittest.TestCase):

    def test_valid_get_by_empty_template(self):
        # This method tests the get_by_template() function
        # to get all groups
        expected = [{'group_id': 1, 'group_name': 'Brian'},
                    {'group_id': 2, 'group_name': 'Tim'},
                    {'group_id': 3, 'group_name': 'Kaan'},
                    {'group_id': 4, 'group_name': 'Ryan'},
                    {'group_id': 5, 'group_name': 'Chi Wu'},
                    {'group_id': 6, 'group_name': 'DELETE TEST'}]

        template = {}
        success, res = GroupResource.get_by_template(template)
        return self.assertEqual(success, True) \
               and self.assertEqual(res, expected)

    def test_valid_get_by_non_empty_template(self):
        # This method tests the get_by_template()
        # passing in a valid group_name
        expected = [{'group_id': 1, 'group_name': 'Brian'}]
        template = {'group_name': "Brian"}
        success, res = GroupResource.get_by_template(
            template)
        return self.assertEqual(success, True) \
               and self.assertEqual(res, expected)

    def test_valid_get_by_non_empty_template(self):
        # This method tests the get_by_template() function
        # passing in a valid group_id
        expected = [{'group_id': 1, 'group_name': 'Brian'}]
        template = {'group_id': 1}
        success, res = GroupResource.get_by_template(template)
        return self.assertEqual(success, True) and self.assertEqual(res, expected)

    def test_valid_insert_by_template(self):
        # This method tests the insert_by_template() function
        # passing in a valid group_name

        # Insert the group
        template = {'group_name': "Group7"}
        success1, _ = GroupResource.insert_by_template(template)

        # Get the group info by get_by_template()
        expected = [{'group_id': 7, 'group_name': 'Group7'}]
        template = {'group_name': 'Group7'}
        success2, res = GroupResource.get_by_template(template)

        correct = self.assertEqual(success1, True) and \
                  self.assertEqual(success2, True) and \
                  self.assertEqual(res, expected)

        return correct

    def test_invalid_insert_by_template(self):
        # This method tests the insert_by_template() function
        # passing in an invalid column name of "name", which
        # is not in the table
        template = {'name': "Group8"}
        success, res = GroupResource.insert_by_template(template)

        return self.assertEqual(success, False)

    def test_valid_delete_by_id(self):
        # This method tests the delete_by_id() function
        # passing in a valid group_id to delete

        # Delete group
        group_id = 7
        success1, res = GroupResource.delete_by_id(group_id)

        # Check if group is deleted by trying to find it in the table
        expected = []
        template = {'group_id': 7}
        success2, res = GroupResource.get_by_template(template)
        return self.assertEqual(success1, True) and self.assertEqual(res, expected)

    def test_valid_add_user_to_group(self):
        # This method tests the add_user_to_group() function,
        # passing in a valid username

        template = {'username': "by2289"}
        group_id = 1

        # For testing, first remove the user if it is already in there
        GroupResource.remove_user_from_group(template, group_id)

        # Add the user to the group
        success1, res = GroupResource.add_user_to_group(template, group_id)
        expected = [{'username': 'by2289',
                     'gmail': 'by2289@columbia.edu',
                     'links': [{'rel': 'self', 'href': '/groups/1'},
                               {'ref': 'username', 'href': '/users/by2289'},
                               {'ref': 'email', 'href': 'by2289@columbia.edu'}]}]

        # Check if user is added to the group by getting all users in the group
        success2, res = GroupResource.get_users(group_id)
        success = self.assertEqual(success1, True) and \
                  self.assertEqual(success2, True) and \
                  self.assertEqual(res, expected)

        return success

    def test_invalid_add_user_to_group(self):
        # This method tests the add_user_to_group() function,
        # trying to add the user to the same group twice, which is invalid
        template = {'username': "by2289"}
        group_id = 2

        GroupResource.remove_user_from_group(template, group_id)

        # Add once
        GroupResource.add_user_to_group(template, group_id)

        # Add again
        success, res = GroupResource.add_user_to_group(template, group_id)
        return self.assertEqual(success, False)

    def test_get_users(self):
        # This method tests the get_user() function,
        # passing in a valid group_id
        group_id = 1
        success, res = GroupResource.get_users(group_id)
        expected = [{'username': 'by2289',
                     'gmail': 'by2289@columbia.edu',
                     'links': [{'rel': 'self', 'href': '/groups/1'},
                               {'ref': 'username', 'href': '/users/by2289'},
                               {'ref': 'email', 'href': 'by2289@columbia.edu'}]}]

        return self.assertEqual(success, True) and self.assertEqual(res, expected)

    def test_invalid_remove_user_from_group(self):
        # This method tests the remove_user_from_group() function
        # passing in an invalid template because 'name' is not a valid
        # column. It has to be 'username'
        template = {'name': "by2289"}
        group_id = 1
        success, res = GroupResource.remove_user_from_group(template, group_id)
        return self.assertEqual(success, False)

    def test_valid_remove_user_from_group(self):
        # This function tests the remove_user_from_group() function,
        # passing in a valid template, to remove by2289 from the group with
        # group_id = 1
        template = {'username': "by2289"}
        group_id = 1
        success, res = GroupResource.remove_user_from_group(template, group_id)
        expected = []
        print("res = ", res)
        return self.assertEqual(success, True) and self.assertEqual(res, expected)

    def test_get_links(self):
        # This method tests the get_links() function, passing in
        # a valid usernames_and_emails dictionary for a user
        usernames_and_emails = [{'username': 'by2289', 'gmail': 'by2289@columbia.edu'}]
        group_id = 1
        success, res = GroupResource.get_links(usernames_and_emails, group_id)
        expected = [{'username': 'by2289',
                     'gmail': 'by2289@columbia.edu',
                     'links': [{'rel': 'self', 'href': '/groups/1'},
                               {'ref': 'username', 'href': '/users/by2289'},
                               {'ref': 'email', 'href': 'by2289@columbia.edu'}]}]
        return self.assertEqual(success, True) and self.assertEqual(res, expected)


if __name__ == '__main__':
    unittest.main()
