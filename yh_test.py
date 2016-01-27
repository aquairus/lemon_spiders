import unittest
import tool.mail
import yahoo_slaver
import yahoo_master
import redis

class Test_slaver(unittest.TestCase):

    def test_ans(self):

        ans_url="https://answers.yahoo.com/question/index?qid=20160121151150AAUBt8O"
        soup=yahoo_slaver.get_soup(ans_url)

        relateQ=yahoo_slaver.find_relateQ(soup)
        self.assertIsInstance(relateQ[0],str)

        title=yahoo_slaver.find_title(soup)
        self.assertIsInstance(title,unicode)

        Qa=yahoo_slaver.find_Qa(soup)
        self.assertIsInstance(Qa,dict)


class Test_master(unittest.TestCase):
    def test_que(self):

        start_url="https://answers.yahoo.com"
        questions,sids=yahoo_master.get_question(start_url)

        self.assertIsInstance(questions,list)




if __name__ == '__main__':
    unittest.main()
