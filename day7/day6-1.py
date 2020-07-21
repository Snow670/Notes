import requests
from bs4 import BeautifulSoup
import time


'''
    58同城
'''
url = 'https://bj.58.com/chuzu'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Cookie':'f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; time_create=1597806785756; userid360_xml=FB6C2DA94129A0B129C64A43AE31D168; BAIDU_SSP_lcr=https://www.baidu.com/baidu.php?sc.0f00000uEDLSpLgiCWybqxlaKe1fTiF8DB_5S7AofaPhzIG0sqgmpUVnZYK8kAmhZq_KXNUiqPvhhpuczHXmInq-ZVyPKFzA-9Bgcv2_l2yT31r43t5r93GV6FwVKEvU0CydWMHACxefdVL30zmxkGNLhJLpEE7XQR7VK4Q9kT_EDrYzy1-Gr-UwYcMTay53Qea_F2oEVcdpCU072PgAc73zw34x.DR_ig4xQI_wKjN63TDZxKfYt_U_DY2ycYlTtUP7nXXqM76133X_X5ik8tXhE_txA1_olx2E_vX5HvyU8MFkl32AM-9uY3vglChcYYp5gKfYt8-P1tA-BZZjdWJIsmt_UArZ-dl-PHV2XgZJyAp7WGtIB60.U1Yz0ZDqPHWg3oXO0ZKGm1Yk0ZfqdS2LEqxH0A-V5HczPfKM5gK1n6KdpHdBmy-bIfKspyfqnfKWpyfqn1T40AdY5HDsnH-xnH0kPdt1nWc3g1nvnjD0pvbqn0KzIjYYPHm0mhbqnHRdg1Ddr7tznjwxnWDL0AdW5HDsnj7xnH6dPjDvn1mvndtknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5HmYnHbdn101nfK8IM0qna3snj0snj0sn0KVIZ0qn0KbuAqs5H00ThCqn0KbugmqTAn0uMfqn0KspjYs0Aq15H00mMTqnH00UMfqn0K1XWY0mgPxpywW5gK1QyPY0A-bm1dRfsKYmgFMugfqn17xn1Dzg1b0IZN15HD1PjR4PWbYnjfYPWmsnHTLrHc10ZF-TgfqnHR4PHczPHb4njnkn6K1pyfquADLnj0knHmsnj0YPADYn6KWTvYqn1u7n1T4rRm1rHmzrj9KnfK9m1Yk0ZK85H00TydY5H00Tyd15H00XMfqn0KVmdqhThqV5HKxn7tsg100uA78IyF-gLK_my4GuZnqn7tsg1c4PWcsP1Nxn0Ksmgwxuhk9u1Ys0AwWpyfqnH0Ln1TYnH6zP0K-IA-b5iYk0A71TAPW5H00IgKGUhPW5H00Tydh5H00uhPdIjYs0A-1mvsqn0KlTAkdT1Ys0A7buhk9u1Yk0Akhm1Ys0AwWmvfq0Zwzmyw-5HR4njckP0KBuA-b5HNAn1m1wbPawHIKP1n3wWRLPHD4fRwDPWcdP1PafWKj0AFY5H00Uv7YI1Ys0AqY5H00ULFsIjYsc10Wc10Wnansc108nj0snj0sc10Wc10WQinsQW0snj0snankQW0snj0sn0KkgLmqna34PNtsQW0sg108njKxna3zn-tsQWDLg108n1n0mMPxTZFEuA-b5H00mLFW5HRknH6k&ck=8373.9.93.304.571.229.590.242&shh=www.baidu.com&sht=baiduhome_pg&us=2.0.1.0.2.768.0&wd=&issp=1&f=8&ie=utf-8&rqlang=cn&tn=baiduhome_pg&sug=58%25E7%25A7%259F%25E6%2588%25BF%25E6%2589%25BE%25E6%2588%25BF%25E6%25BA%2590&inputT=3808&bc=110101; myLat=""; myLon=""; id58=z5vesl8VC7eoYBYbjW6VQQ==; mcity=bj; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; city=bj; 58home=bj; 58tj_uuid=4f8e7f3a-e2e4-41dc-a0d4-3d4930f90b88; als=0; wmda_new_uuid=1; wmda_uuid=26c707fb672e72a860d2af77e4ceeb7d; wmda_visited_projects=%3B11187958619315; xxzl_deviceid=1wlGIboWbpahyeOaesVBUj8lBbpOZqsO4rmQxYg3VL9DXmJ53FVbl6%2FP37TFWgnk; wmda_session_id_11187958619315=1595225999988-0d467d43-285d-5c2b; new_uv=2; utm_source=sem-sales-baidu-pc; spm=57614770416.14876405623; init_refer=https%253A%252F%252Fwww.baidu.com%252Fbaidu.php%253Fsc.0f00000uEDLSpLgiCWybqxlaKe1fTiF8DB_5S7AofaPhzIG0sqgmpUVnZYK8kAmhZq_KXNUiqPvhhpuczHXmInq-ZVyPKFzA-9Bgcv2_l2yT31r43t5r93GV6FwVKEvU0CydWMHACxefdVL30zmxkGNLhJLpEE7XQR7VK4Q9kT_EDrYzy1-Gr-UwYcMTay53Qea_F2oEVcdpCU072PgAc73zw34x.DR_ig4xQI_wKjN63TDZxKfYt_U_DY2ycYlTtUP7nXXqM76133X_X5ik8tXhE_txA1_olx2E_vX5HvyU8MFkl32AM-9uY3vglChcYYp5gKfYt8-P1tA-BZZjdWJIsmt_UArZ-dl-PHV2XgZJyAp7WGtIB60.U1Yz0ZDqPHWg3oXO0ZKGm1Yk0ZfqdS2LEqxH0A-V5HczPfKM5gK1n6KdpHdBmy-bIfKspyfqnfKWpyfqn1T40AdY5HDsnH-xnH0kPdt1nWc3g1nvnjD0pvbqn0KzIjYYPHm0mhbqnHRdg1Ddr7tznjwxnWDL0AdW5HDsnj7xnH6dPjDvn1m; new_session=0; xxzl_cid=1fc8197ef4ac454fa1c1dcfb4353a9dd; xzuid=6191e693-2515-4386-922b-ab34973e4c47'
}
# 设置header
web_data = requests.get(url, headers=headers)
 
time.sleep(4)
soup = BeautifulSoup(web_data.text, 'lxml')
 
titles = soup.select('body > div.list-wrap > div.list-box > ul > li > div.des > h2 > a')
for title in titles:
    print(title.get_text())
 
 
# 移动端的反扒策略相比较PC简单


'''
    链家
'''

import requests
from bs4 import BeautifulSoup
import lxml
 
def get_html():
    url = 'https://bj.lianjia.com/zufang' 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    titles = soup.select('div.content__article > div.content__list > div > div > p.content__list--item--title.twoline > a')
    for title in titles:
        print(title.get_text())
 
 
get_html()