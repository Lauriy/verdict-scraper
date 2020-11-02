import io
import os

import responses

from check_if_followups import ping_single_verdict

test_html = io.open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/240199396.html', encoding='utf-8').read()


@responses.activate
def test_ping_single_verdict():
    responses.add(responses.GET, 'https://www.riigiteataja.ee/kohtulahendid/detailid.html?id=240199396', body=test_html)
    ping_single_verdict(240199396)
