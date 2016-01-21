import requests
import yaml
from bs4 import BeautifulSoup
from pprint import pprint as pp

class Harvester(object):
    # setup the harvester
    def __init__(self, ruleset='rules.yml', verbose=False):
        self.base_url = 'https://en.wikipedia.org/wiki/'
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
    def extract(self, w_id, rules): #this receives the url of the list page
        page = self.get(w_id)
        soup = BeautifulSoup(page, 'html.parser')
        links_from_page = set()
        for scope in rules['scopes']:
            subsection = soup.select(scope)
            for link in subsection:
                url = link.get('href')
                topic = self.evaluate_topic_url(url, rules)
                if topic:
                    links_from_page.add(topic)
        return links_from_page
        
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

    #TODO: this should generate a list and return it rather than setting an instance property that gets collected in main. Just a better design
    # work through the ruleset
    def crawl(self):
        seeds = self.ruleset['seeds']
        links_from_root_lists = set()
        for w_id, rules in seeds.items():#so basically the w_id is each entry in the "seeds" list (just 2 of them at the moment). and rules is everything underneath each w_id. at the moment only "scopes". also at the moment each scopes only has one entry
           links_from_root_lists = links_from_root_lists.union(self.extract(w_id, rules))
        #we finished gathering all of the topics, so return them
        return links_from_root_lists

def main():
    harvester = Harvester()
    harvester.verbose = True
    # do something with the resulting topics
    pp(list(harvester.crawl()))

if __name__ == '__main__':
    main()
    print("program finished naturally...")