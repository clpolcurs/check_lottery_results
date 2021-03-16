__doc__ = """
Make a script to check whether arguments match the someday lottery's result (only the last 2 digits of the resuls). If there's no argument input, print the results of that day.

Crawl results from `ketqua.net`.

Command prompt:

  check_lottery_results.py [NUMBER1] [NUMBER2] [...]
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
    # using "lxml" for speed issue instead of "html.parser"
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    # get all the ids from soup which start with 'rs' including rs_0_0 that stands for no prize
    list_of_ids = [tag['id'] for tag in soup.select(
        'div[id]') if tag['id'].startswith('rs')]
    results = []
    for id in list_of_ids:
        result = soup.find(attrs={'id': '{}'.format(id)}).text
        results.append(result)

    return results[1:]  # get rid of rs_0_0


def solve(*args):
    count = 0
    for number in args:
        # compare to the list of 2 last digits of prizes
        if number[-2:] in [result[-2:] for result in get_prizes()]:
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
