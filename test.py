import unittest
import mail

class Testmail(unittest.TestCase):

    def setUp(self):
        mail_user=raw_input("mail?")
        mail_pass=raw_input("passwd?")
        self.box=mail.mailbox(mail_user,mail_pass)
        print('setUp...')


    def test_init(self):
        state=self.box.login()
        self.assertEqual(state[0], 235)
        box.send_msg("sender","hello")

    def tearDown(self):
        print('tearDown...')

if __name__ == '__main__':
    unittest.main()
