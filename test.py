import unittest
import mail
import yahoo_slaver
import redis
import yahoo_master
# class Test_mail(unittest.TestCase):
#
#     def setUp(self):
#         mail_user=raw_input("mail?")
#         mail_pass=raw_input("passwd?")
#         self.box=mail.mailbox(mail_user,mail_pass)
#         print('setUp...')
#
#
#     def test_init(self):
#         state=self.box.login()
#         self.assertEqual(state[0], 235)
#         box.send_msg("sender","hello")
#
#     def tearDown(self):
#         print('tearDown...')


# class Test_slaver(unittest.TestCase):
#
#     def test_ans(self):
#         ans_url="https://answers.yahoo.com/question/index?qid=20160121151150AAUBt8O"
#         soup=yahoo_slaver.get_soup(ans_url)
#
#         relateQ=yahoo_slaver.find_relateQ(soup)
#         self.assertIsInstance(relateQ[0],str)
#
#         title=yahoo_slaver.find_title(soup)
#         self.assertIsInstance(title,unicode)
#
#         Qa=yahoo_slaver.find_Qa(soup)
#         self.assertIsInstance(Qa,dict)
#
#         r = redis.StrictRedis(host='spider01', port=6369, db=0)
#         yahoo_slaver.commit_link(r,"test_Q",relateQ)
#         test_relateQ=yahoo_slaver.fetch_link(r,"test_Q",len(relateQ))
#         self.assertEqual(test_relateQ,relateQ)

# class Test_master(unittest.TestCase):
#     def test_que(self):
#         start_url="https://answers.yahoo.com"
#         questions,sids=yahoo_master.get_question(start_url)
#         q_list=yahoo_master.ques_factory(2,sids)
#         self.assertIsInstance(questions,list)
#         self.assertIsInstance(q_list,list)

# class Testredis(unittest.TestCase):
#
#     def test_ini(self):
#         r = redis.StrictRedis(host='spider01', port=6369, db=0)
#         r.set('foo', 'bar')
#         self.assertEqual('bar',r.get('foo'))

if __name__ == '__main__':
    unittest.main()
