import io
import os

import responses

from check_if_followups import ping_single_verdict

test_html = io.open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/240778738.html', encoding='utf-8').read()
test_html_2 = io.open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/247765253.html', encoding='utf-8').read()


@responses.activate
def test_ping_single_verdict():
    responses.add(responses.GET, 'https://www.riigiteataja.ee/kohtulahendid/detailid.html?id=240778738', body=test_html)
    responses.add(responses.GET, 'https://www.riigiteataja.ee/kohtulahendid/detailid.html?id=247765253',
                  body=test_html_2)
    end_url = ping_single_verdict(240778738)

    assert end_url == 'https://www.riigiteataja.ee/kohtulahendid/detailid.html?id=247765253'
