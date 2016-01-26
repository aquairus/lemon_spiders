import unittest
import naver





class Testredis(unittest.TestCase):

    def test_ini(self):
        r = redis.StrictRedis(host='spider01', port=6369, db=0)
        r.set('foo', 'bar')
        self.assertEqual('bar',r.get('foo'))

if __name__ == '__main__':
    unittest.main()
