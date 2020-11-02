import concurrent.futures
import os
import re

import bs4
import requests


def ping_single_verdict(verdict_id: int):
    url = f'https://www.riigiteataja.ee/kohtulahendid/detailid.html?id={verdict_id}'

    response = requests.get(url)
    if 'Seotud lahendid' in response.text:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        case_number_a = soup.find_all('a', href=re.compile('/kohtulahendid/fail.html'))[0]
        inner_id = int(case_number_a.contents[0].split('/')[1])
        related_case_number_as = soup.find_all('a', href=re.compile('detailid.html\\?id'))
        for each in related_case_number_as:
            related_inner_id = int(each.contents[0].split('/')[1])
            if related_inner_id > inner_id:
                print(f'Verdict {verdict_id} has follow-up verdicts')


def run_over_all_files():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ids = [x.split('.')[0] for x in os.listdir('./verdicts') if x.endswith('pdf')]
        responses = [executor.submit(ping_single_verdict, verdict_id) for verdict_id in ids]
        concurrent.futures.wait(responses)

# for response in responses:
#     print(response.result())
