
from settings import USER_AGENT_LIST,cookies
import random




cookies={"c_user":"100011698728234",
"csm":"2",
"datr:B0EPV-vzabw01XSOiDbPoRbA,
"fr":"0IdhVLF5E5Rzvpp2k.AWXshiFFSV9xNJtLDbAAL8zCSCM.BXD0fL.Zq.AAA.0.AWXtjpKC",
"locale":"zh_CN",
"lu":"RgBQDUfzKadnVjiobkkx_6HA",
"m_user":"0%3A0%3A0%3A0%3Av_1%2Cajax_0%2Cwidth_0%2Cpxr_0%2Cgps_0%3A1460619211%3A2",
"s":"Aa5Q0D_-DsbAgVFV.BXD0fL",
"sb":"y0cPV-vxzyVeLy2AMl08919a",
"x-src":'%2Fpeople%2F%25D8%25B3%25D8%25A7%25D9%2585%25D8%25B1-%25D8%25A7%25D9%2584%25D8%25B3%25D8%25B9%25D9%258A%25D8%25AF%2F100005145335207%7Cpage_footer',
"xs":"167%3A75hklqrBothiyA%3A2%3A1460619211%3A-1"}



class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):

        ua  = random.choice(USER_AGENT_LIST)
        print ua
        if ua:
            request.headers.setdefault('User-Agent', ua)
        request.cookies=cookies
        print cookies#request.cookies
