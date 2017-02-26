from siteretriever import ListingsRetriever, SiteRetriever
# from reportbuilder import (WordCountReportBuilder, HeaderReportBuilder,
#                            PerformanceReportBuilder)
from reportbuilder import ReportBuilder
from timer import timethis

def gather_alexa_data(name, password):
    """
    Retrieve data for the top 100 sites on Alexa.

    Data includes word count, headers, cookies and the time it took
    to gather the data.
    """
    l = ListingsRetriever(name, password)
    listings = l.get_listings()
    s = SiteRetriever()
    alexa_sites_data = s.build_sites_list(listings)
    return alexa_sites_data

def build_reports(alexa_sites_data, builders, file_format):
    """
    Creates a new report from each of the passed report builders.
    """
    for Builder in builders:
        report_builder = Builder(alexa_sites_data)
        report_builder.create_report(file_format)

def main(name, password, builders, file_format):
    alexa_data = gather_alexa_data(name, password)
    build_reports(alexa_data, builders, file_format)

if __name__ == "__main__":
    # import sys
    # name = sys.argv[1]
    # password = sys.argv[2]
    # builders = [WordCountReportBuilder, HeaderReportBuilder,\
    #             PerformanceReportBuilder]
    file_format = "html"

    listings = ["google.com", "bing.com"]

    s = SiteRetriever()
    data = s.build_sites_list(listings)
    categories = ["site_name", "word_count"]
    report_builder = ReportBuilder("some report", categories, data)
    report_builder.create_report(file_format)

    # main(name, password, builders, file_format)
