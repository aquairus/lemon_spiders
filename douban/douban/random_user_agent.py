
from settings import USER_AGENT_LIST
import random


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        print ua
        if ua:
            request.headers.setdefault('User-Agent', ua)
