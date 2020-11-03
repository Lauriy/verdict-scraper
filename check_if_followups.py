import concurrent.futures
import os
import re

import bs4
import requests


def ping_single_verdict(verdict_id: int):
    url = f'https://www.riigiteataja.ee/kohtulahendid/detailid.html?id={verdict_id}'

    response = requests.get(url)
    if 'Apellatsioonmenetlus' in response.text:
        return url
    if 'Seotud lahendid' in response.text:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        case_number_a = soup.find_all('a', href=re.compile('/kohtulahendid/fail.html'))[0]
        case_number_parts = case_number_a.contents[0].split('/')
        main_case_number = case_number_parts[0]
        current_case_number_subcase = int(case_number_parts[1])
        related_case_number_as = soup.find_all('a', href=re.compile('detailid.html\\?id'))
        max_related_subcase_id = 0
        max_subcase_link = None
        for each in related_case_number_as:
            a_contents = each.contents[0]
            a_contents = a_contents.replace('\\', '/')
            if a_contents.startswith(main_case_number):
                related_subcase_number = int(a_contents.split('/')[1])
                if related_subcase_number > max_related_subcase_id and related_subcase_number > current_case_number_subcase:
                    max_related_subcase_id = related_subcase_number
                    max_subcase_link = f'https://www.riigiteataja.ee/kohtulahendid/{each.attrs["href"]}'

        if max_subcase_link:
            subresponse = requests.get(max_subcase_link)
            if 'Apellatsioonmenetlus' in subresponse.text:
                return max_subcase_link


def run_over_all_files():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ids = [x.split('.')[0] for x in os.listdir('./verdicts') if x.endswith('pdf')]
        responses = [executor.submit(ping_single_verdict, verdict_id) for verdict_id in ids]
        concurrent.futures.wait(responses)

    with open('with_followups.txt', 'w') as opened_file:
        for response in responses:
            result = response.result()
            if result is not None:
                opened_file.write(result + '\n')


def main():
    run_over_all_files()


if __name__ == '__main__':
    main()
