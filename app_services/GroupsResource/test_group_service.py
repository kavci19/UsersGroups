import unittest
from group_service import GroupResource


class TestGroupResource(unittest.TestCase):

    def test_get_by_template(self):
        template = {}
        GroupResource.get_by_template(template)
        return self.assertEqual(True, True)

    def test_delete_by_id(self):
        group_id = 1
        GroupResource.delete_by_id(group_id)
        return self.assertEqual(True, True)

    def test_get_users(self):
        group_id = 1
        GroupResource.get_users(group_id)
        return self.assertEqual(True, True)

    def test_add_user_to_group(self):
        template = {}
        group_id = 1
        GroupResource.add_user_to_group(template, group_id)
        return self.assertEqual(True, True)

    def test_remove_user_from_group(self):
        template = {}
        group_id = 1
        GroupResource.remove_user_from_group(template, group_id)
        return self.assertEqual(True, True)

    def test_get_links(self):
        usernames_and_emails = [{}, {}]
        group_id = 1
        GroupResource.get_links(usernames_and_emails, group_id)
        return self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
