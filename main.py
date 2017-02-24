from siteretriever import ListingsRetriever, SiteRetriever
from reportbuilder import (WordCountReportBuilder, HeaderReportBuilder,
                           PerformanceReportBuilder)
from timer import timethis

def gather_alexa_data(name, password, builders):
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

def build_reports(alexa_sites_data, builders):
    """
    Creates a new report from each of the passed report builders.
    """
    for Builder in builders:
        report_builder = Builder(alexa_sites_data)
        report_builder.create_report()

def main(name, password):
    alexa_data = gather_alexa_data(name, password)
    build_reports(alexa_data)

if __name__ == "__main__":
    import sys
    name = sys.argv[1]
    password = sys.argv[2]
    builders = [WordCountReportBuilder, HeaderReportBuilder,\
                PerformanceReportBuilder]
    main(name, password, builders)
