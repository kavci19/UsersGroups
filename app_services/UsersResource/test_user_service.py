import unittest
from user_service import UserResource


class Test_TestUserService(unittest.TestCase):

    def test(self):
        res = UserResource.get_by_template({})
        print(res)
        return self.assertEquals(True, True)




if __name__ == '__main__':
    unittest.main()
