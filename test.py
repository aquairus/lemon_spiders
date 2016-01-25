import unittest
import mail
import yahoo_slaver

# class Testmail(unittest.TestCase):
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


class Testslaver(unittest.TestCase):

    def test_ans(self):
        ans_url="https://answers.yahoo.com/question/index?qid=20160121151150AAUBt8O"
        soup=yahoo_slaver.get_soup(ans_url)
        answers=yahoo_slaver.find_answer(soup)
        self.assertIsInstance(answers[0],list)

        relateQ=yahoo_slaver.find_relateQ(soup)
        self.assertIsInstance(relateQ[0],str)

        title=yahoo_slaver.find_title(soup)
        self.assertIsInstance(title,unicode)

        Qa=yahoo_slaver.find_Qa(soup)
        self.assertIsInstance(Qa,dict)



if __name__ == '__main__':
    unittest.main()
