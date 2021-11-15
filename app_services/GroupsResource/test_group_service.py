import unittest
from group_service import GroupResource


class TestGroupResource(unittest.TestCase):

    def test_valid_get_by_empty_template(self):
        expected = [{'group_id': 1, 'group_name': 'Brian'},
                    {'group_id': 2, 'group_name': 'Tim'},
                    {'group_id': 3, 'group_name': 'Kaan'},
                    {'group_id': 4, 'group_name': 'Ryan'},
                    {'group_id': 5, 'group_name': 'Chi Wu'},
                    {'group_id': 6, 'group_name': 'DELETE TEST'}]

        template = {}
        success, res = GroupResource.get_by_template(template)
        return self.assertEqual(success, True) and self.assertEqual(res, expected)

    def test_valid_get_by_non_empty_template(self):
        expected = [{'group_id': 1, 'group_name': 'Brian'}]
        template = {'group_name': "Brian"}
        success, res = GroupResource.get_by_template(template)
        return self.assertEqual(success, True) and self.assertEqual(res, expected)

    def test_valid_get_by_non_empty_template(self):
        expected = [{'group_id': 1, 'group_name': 'Brian'}]
        template = {'group_id': 1}
        success, res = GroupResource.get_by_template(template)
        print("res = ", res)
        return self.assertEqual(success, True) and self.assertEqual(res, expected)

    def test_valid_insert_by_template(self):
        template = {'group_id': 7,
                    'group_name': "Group7"}
        success1, _ = GroupResource.insert_by_template(template)

        expected = [{'group_id': 7, 'group_name': 'Group7'}]
        template = {'group_id': 7}
        success2, res = GroupResource.get_by_template(template)

        correct = self.assertEqual(success1, True) and \
                  self.assertEqual(success2, True) and \
                  self.assertEqual(res, expected)
        return correct

    # def test_delete_by_id(self):
    #     group_id = 1
    #     GroupResource.delete_by_id(group_id)
    #     return self.assertEqual(True, True)
    #
    # def test_get_users(self):
    #     group_id = 1
    #     GroupResource.get_users(group_id)
    #     return self.assertEqual(True, True)
    #
    # def test_add_user_to_group(self):
    #     template = {}
    #     group_id = 1
    #     GroupResource.add_user_to_group(template, group_id)
    #     return self.assertEqual(True, True)
    #
    # def test_remove_user_from_group(self):
    #     template = {}
    #     group_id = 1
    #     GroupResource.remove_user_from_group(template, group_id)
    #     return self.assertEqual(True, True)
    #
    # def test_get_links(self):
    #     usernames_and_emails = [{}, {}]
    #     group_id = 1
    #     GroupResource.get_links(usernames_and_emails, group_id)
    #     return self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
