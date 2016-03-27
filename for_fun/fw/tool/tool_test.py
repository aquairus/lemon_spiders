import unittest
import redis
import mail
class Test_mail(unittest.TestCase):

    def setUp(self):
        mail_user=raw_input("mail?")
        mail_pass=raw_input("passwd?")
        self.box=mail.mailbox(mail_user,mail_pass)
        print('setUp...')


    def test_init(self):
        state=self.box.login()
        self.assertEqual(state[0], 235)
        box.send_msg("sender","hello")

class Testredis(unittest.TestCase):

    def test_ini(self):
        r = redis.StrictRedis(host='spider01', port=6369, db=0)
        r.set('foo', 'bar')
        self.assertEqual('bar',r.get('foo'))


if __name__ == '__main__':
    unittest.main()
