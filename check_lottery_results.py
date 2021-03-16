__doc__ = """
Viết một script kiểm tra xem các số argument đầu vào có trúng lô không
(2 số cuối trùng với một giải nào đó). Nếu không có argument nào thì print
ra tất cả các giải từ đặc biệt -> giải 7.

Lấy kết quả từ ``ketqua.net``.

Dạng của câu lệnh::

  ketqua.py [NUMBER1] [NUMBER2] [...]

Các thư viện:

- requests
- requests_html hay beautifulsoup4 [tuỳ chọn]
- argparse hay sys.argv

Gợi ý:

- ``nargs`` https://docs.python.org/2/library/argparse.html
"""

import requests
import bs4
import sys
from datetime import date

today = date.today()
date = today.strftime('%m/%d/%y')


def get_prizes():
    ses = requests.session()
    req = ses.get('http://ketqua.net/')
    soup = bs4.BeautifulSoup(req.text, 'lxml')                                                 #using "lxml" for speed issue instead of "html.parser"
    list_of_ids = [tag['id'] for tag in soup.select('div[id]') if tag['id'].startswith('rs')]  #get all the ids from soup which start with 'rs' including rs_0_0 that stands for no prize
    results = []
    for id in list_of_ids:
        result = soup.find(attrs={'id': '{}'.format(id)}).text
        results.append(result)
    
    return results[1:]                                                                         #get rid of rs_0_0

def solve(*args):    
    count = 0
    for number in args:
        if number[-2:] in [result[-2:] for result in get_prizes()]:                            # compare to the list of 2 last digits of prizes
            count += 1
            print('Congrat! {} is your lucky number!'.format(number))
    if count == 0:
        print("You screw it up! Maybe next times.\n Today {} `s numbers are: ".format(date))
        print(", ".join(get_prizes()))


def main():
    args = [sys.argv[i] for i in range(1, len(sys.argv))]
    if len(sys.argv) == 1:
        print("Today {} `s numbers are: ".format(date))
        print(", ".join(get_prizes()))
    else:
        print(solve(*args))


if __name__ == "__main__":
    main()