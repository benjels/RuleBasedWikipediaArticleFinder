import requests
import yaml
from bs4 import BeautifulSoup
from pprint import pprint as pp

class Harvester(object):
    # setup the harvester
    def __init__(self, ruleset='rules.yml', verbose=False):
        self.base_url = 'https://en.wikipedia.org/wiki/'
        # use set rather than list to ensure uniqueness
        self.topics = set()
        # rules tell the harvester what lists pages to grab
        # and how to evaluate urls on that page
        with open(ruleset, 'r') as stream:
            self.ruleset = yaml.load(stream)
        self.verbose = verbose

    # get a wikipedia page
    def get(self, w_id):
        url = self.base_url + w_id
        if self.verbose:
            print('Fetching: {}'.format(url))
        r = requests.get(url)
        if r.status_code != 200:
            print('Error: {}.'.format(r.status_code))
            return None
        return r.content

    # extract links from a wikipedia page
    def extract(self, w_id, rules):
        page = self.get(w_id)
        soup = BeautifulSoup(page, 'html.parser')
        for scope in rules['scopes']:
            subsection = soup.select(scope)
            for link in subsection:
                url = link.get('href')
                topic = self.evaluate_topic_url(url, rules)
                if topic:
                    self.topics.add(topic)
        
    # check whether a topic url meets our rules
    def evaluate_topic_url(self, url, rules):
        # test if url has wiki in it
        if not '/wiki/' in url:
            return None
        # test if url contains an ignore string
        lower_url = url.lower()
        if any(el in lower_url for el in self.ruleset['ignore']):
            return None

        return url.replace('/wiki/', '')

    # work through the ruleset
    def crawl(self):
        seeds = self.ruleset['seeds']
        for w_id, rules in seeds.items():
            self.extract(w_id, rules)

def main():
    harvester = Harvester()
    harvester.verbose = True
    harvester.crawl()
    # do something with the resulting topics
    pp(list(harvester.topics))

if __name__ == '__main__':
    main()