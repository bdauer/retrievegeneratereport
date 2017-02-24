import unittest
from reportbuilder import ReportBuilder, WordCountReportBuilder
from siteretriever import ListingsRetriever, SiteRetriever
from test_data import alexa_text, alexa_listings
import requests
import requests_mock
from bs4 import BeautifulSoup


class BuilderTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        data = [{"site_name":"apple",
                "headers": ["five", "four", "three"],
                "cookies": [],
                "word_count": 42},
                {"site_name":"pear",
                "headers": ["a", "b", "c"],
                "cookies": ["oreo", "choc_chip", "hermit"],
                "word_count": 145}]
        self.r = ReportBuilder(data)

        self.plain_table = """<table border="1">
                    <tr><th>Ranking</th></tr>
                    <tr><td>1</td></tr>
                    <tr><td>2</td></tr>
                    </table>""".replace("\n", "").replace(" ", "")

        self.plain_report = """<head><title>Report</title></head>
        <body><h2>Report</h2><br>{0}<br><br><br></body>
        """.format(self.plain_table).replace("\n", "").replace(" ", "")

        self.wcr = WordCountReportBuilder(data)

        self.wcr_table = """<table border="1">
                    <tr><th>Ranking</th><th>site name</th><th>word count</th></tr>
                    <tr><td>1</td><td>apple</td><td>42</td></tr>
                    <tr><td>2</td><td>pear</td><td>145</td></tr>
                    <tr><td><b>average word count:</b></td><td><b>93.5</b></td></tr>
                    </table>""".replace("\n", "").replace(" ", "")

    def test_plain_table(self):
        plain_table = self.r.build_table().replace("\n", "").replace(" ", "")
        self.assertEqual(plain_table, self.plain_table)

    def test_plain_report(self):
        plain_report = self.r.build_report().replace("\n", "").replace(" ", "")
        self.assertEqual(plain_report, self.plain_report)


    def test_word_count_table(self):
        wcr_table = self.wcr.build_table().replace("\n", "").replace(" ", "")
        self.assertEqual(wcr_table, self.wcr_table)

class ListingsRetrieverTestCase(unittest.TestCase):

    def setUp(self):
        self.lr = ListingsRetriever("me@me.com", "secret")

        soup = BeautifulSoup(alexa_text, 'html.parser')
        listings_table = soup.find("div", "listings table")
        page_listings = listings_table.find_all("div", "site-listing")
        self.soupy_listings = list(page_listings)

    def test_scrub_listings(self):
        scrubbed_listings = self.lr._scrub_listings(self.soupy_listings)
        self.assertEqual(scrubbed_listings, alexa_listings)

class SiteRetrieverTestCase(unittest.TestCase):

    def setUp(self):
        self.sr = SiteRetriever()

        adapter = requests_mock.Adapter()
        adapter.register_uri('GET',
                             'mock://google.com',
                             headers={"headerkey":"someval"},
                             cookies={"choc_chip":"ok"},
                             text="two words")
        session = requests.Session()
        session.mount('mock', adapter)
        self.resp = session.get("mock://google.com")

    def test_get_data_from(self):
        headers, cookies, word_count = self.sr._get_data_from(self.resp)
        self.assertEqual(headers, ["headerkey"])
        self.assertEqual(cookies, ["choc_chip"])
        self.assertEqual(word_count, 2)

    def test_build_site_dictionary(self):
        generated_dict = self.sr._build_site_dictionary(self.resp, "google.com")
        # using assertIn instead of assertEqual
        # because the timethis decorator adds a dynamic value to the dictionary.
        # could have also deleted or overwritten 'time_to_complete'
        self.assertIn(("site_name", 'google.com'), generated_dict.items())
        self.assertIn(("headers", ['headerkey']), generated_dict.items())
        self.assertIn(("cookies", ['choc_chip']), generated_dict.items())
        self.assertIn(("word_count", 2), generated_dict.items())










if __name__ == '__main__':
    unittest.main()
