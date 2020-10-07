import requests
from bs4 import BeautifulSoup
import re
import os

site_url = 'https://www.cts-tradeit.cz'
career_url = site_url + "/kariera"
save_folder = 'job_profiles'

def get_job_urls(page):
    urls = []
    for tag_a in page.find_all('a'):
        href = tag_a.get('href', '')
        if href.startswith('/kariera/') and href != '/kariera/':
            urls.append(site_url + href)
    return urls

def save_to_file(filepath, text):
    with open(filepath, 'wb') as fp:
        fp.write(text.encode('utf-8'))

def sanitize_filename(filename):
    return re.sub('[\s]', '_', re.sub('[./]', '', filename))

def get_page_html(url):
    return requests.get(url).content

if __name__ == '__main__':
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    career_page = BeautifulSoup(get_page_html(career_url), 'html.parser')

    print('Getting job links...')
    for url in get_job_urls(career_page):
        job_page = BeautifulSoup(get_page_html(url), 'html.parser')

        description = job_page.find('div', class_='story__text').text.strip()
        name = job_page.find('div', class_='hero__text').text.strip().lower()
        filepath = os.path.join(save_folder, sanitize_filename(name) + '.txt')

        print(f'Saving job to the file {filepath}')
        save_to_file(filepath, description)



