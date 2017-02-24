from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
from timer import timethis

class ListingsRetriever:
    """
    Class for retrieving top listings from Alexa.
    """
    BASE_URL = "http://www.alexa.com/topsites/global;"
    LOGIN_URL = "http://www.alexa.com/secure/login/ajaxex"

    def __init__(self, email, password, num_sites=100):
        self.email = email
        self.password = password
        self.num_sites = num_sites
        self.num_pages = self._get_number_of_amazon_pages(num_sites)

    def get_listings(self):
        """
        Return a list of the top Alexa sites.
        """
        print("Retrieving top sites from Alexa...")
        soupy_listings = self._get_soupy_listings()
        top_sites = self._scrub_listings(soupy_listings)
        print("Top sites retrieved...")
        return top_sites

    def _get_number_of_amazon_pages(self, num_sites):
        """
        Return the number of amazon pages to visit.

        Since there are 25 results per page,
        and a user might want a number of results
        that is not a multiple of 25,
        this method ensures
        that any desired results over the multiple
        are still retrieved.

        It's not necessary for the naive implementation
        but it will make future enhancements easier
        by maintaining abstraction.
        """
        if num_sites % 25 == 0:
            return num_sites // 25
        else:
            return (num_sites // 25) + 1

    def _get_soupy_listings(self):
        """
        Return a list of site listings,
        still made of soup.
        """
        with requests.Session() as s:
            payload = {'email': self.email, 'password': self.password, 'async': 'async', "type": "object"}
            p = s.post(self.LOGIN_URL, data=payload)
            # need to visit a second time to get a successful login.
            p = s.post(self.LOGIN_URL, data=payload)
            print(p.content)

            soupy_listings = []
            for number in range(self.num_pages):
                page = s.get(self.BASE_URL + str(number))
                soup = BeautifulSoup(page.text, 'html.parser')
                listings_table = soup.find("div", "listings table")
                page_listings = listings_table.find_all("div", "site-listing")
                soupy_listings.extend(page_listings)
            return soupy_listings

    def _scrub_listings(self, soupy_listings):
        """
        Return a list of sites
        equal in number to self.num_sites.
        """
        sites = []
        for listing in soupy_listings[:self.num_sites]:
            description = listing.find("div", "td DescriptionCell")
            unclean_site = description.p.get_text()
            scrubbed_site = unclean_site.strip()
            sites.append(scrubbed_site)
        return sites

class SiteRetriever:
    """
    Class for retrieving data from a list of sites.
    """

    def build_sites_list(self, listings):
        """
        Return a list of site dictionaries.
        """
        print("Collecting sites data...")
        sites_list = []
        for site in listings:
            print("Collecting {0}'s data...".format(site))
            sites_list.append(self._build_site_dictionary(site))
        print("Sites data collected...")
        return sites_list
    @timethis
    def _build_site_dictionary(self, site):
        """
        Return a site dictionary.
        """
        headers, cookies, word_count = self._get_data_from(site)
        return {
            "site_name": site,
            "headers": headers,
            "cookies": cookies,
            "word_count": word_count}

    def _get_data_from(self, site):
        """
        Return all of the data retrieved from site.

        site: the url for a website sans protocol.
        """
        try:
            url = "http://" + site
            page = requests.get(url)
        except requests.exceptions.SSLError:
            url = "http://www." + site
            page = requests.get(url)
        headers = list(page.headers.keys())
        cookies = page.cookies.keys()
        word_count = self._get_wordcount(page)

        return (headers, cookies, word_count)

    def _get_wordcount(self, page):
        """
        Return the number of words on a page.
        """
        soup = BeautifulSoup(page.text, 'html.parser')
        words = soup.get_text().split()
        return len(words)
