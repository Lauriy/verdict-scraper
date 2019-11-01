import bs4
import requests

search_template = 'https://www.riigiteataja.ee/kohtulahendid/otsingutulemus.html?leht=%s&lahendiTekst=' \
                  '&lahendiKpvLopp=01.11.2019&kohtunik=&sort=LahendiKuulutamiseAeg&menetluseKpvLopp=' \
                  '&lahendiKpvAlgus=01.01.2019&aktiivneTab=KOIK&asc=false&kohtuasjaNumber=&lahendiLiik=' \
                  '&kohus=1989&menetluseLiik=&annotatsiooniSisu=&menetluseKpvAlgus=&ecliNumber='

for page in range(1, 771):
    print(page)
    response = requests.get(search_template % str(page))
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    table = soup.select('.data')[0]
    for row in soup.select('tr')[1:]:
        links = row.select('a')
        file_url = 'https://www.riigiteataja.ee' + links[1].get('href')
        id = file_url.split('id=')[1]
        with open('verdicts/%s.pdf' % id, 'wb') as f:
            f.write(requests.get(file_url).content)
