import urllib3
from bs4 import BeautifulSoup

def retrieve_versionsOS(os):
    url = 'https://app.vagrantup.com/' + os
    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')
    boxes = soup.findAll('div', {'class': 'col-md-6'})
    versions = []
    for box in boxes:
        version = box.text.split()[0]
        description = box.text.rsplit('\n', 3)[2][12:]
        versions.append((version, description))
    return versions
