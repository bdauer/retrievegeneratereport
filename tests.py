from reportbuilder import ReportBuilder, WordCountReportBuilder
from siteretriever import ListingsRetriever, SiteRetriever
import unittest


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
        l = ListingsRetriever("me@me.com", "secretpassword")

        # test get_listings with a mock site


class SiteRetrieverTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # test build sites list with a mock site.


if __name__ == '__main__':
    unittest.main()
