import unittest
import tool.mail
import naver
import Queue


class Test_slaver(unittest.TestCase):

    def test_ans(self):


        ans_url="http://kin.naver.com/qna/detail.nhn?d1id=11&dirId=110408&docId=243351741"

        soup=naver.get_soup(ans_url)
        Links=naver.get_relateQ(soup)
        self.assertIsInstance(Links[0],str)

        # title=yahoo_slaver.find_title(soup)
        # self.assertIsInstance(title,unicode)
        #
        # Qa=yahoo_slaver.find_Qa(soup)
        # self.assertIsInstance(Qa,dict)





if __name__ == '__main__':
    unittest.main()
