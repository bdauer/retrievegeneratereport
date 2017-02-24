## Description

This program collects the names of the top 100 sites on Alexa.

It accesses each site, collecting:
    * the total word count of the site's landing page
    * the site's header keys
    * the site's cookie keys

For each site, the script times how long it took to access the page and gather data.

It outputs three HTML reports in table format:
    * A report of word count by site, including an average of all sites.
    * A report of headers and cookies by site.
    * A report of the time taken to access each site, and the total program performance time.


## Considered Enhancements
* Get better test coverage.
* find the most common cookie and header names, excluding the most typical headers.
* Detect the language for each site.
* Generate a score based on the ratio of words to ranking.
* Generate a score based on the ratio of ranking to performance.
* Abstract the SiteRetriever and ListingsRetriever classes a bit, and create a base class for each of them to inherit from. This would allow a more consistent interface for generating data that a subclass of ReportBuilder could consume.
* I might consider abstracting out the categories used for column creation, but in order for that to an effective way to reduce the need for subclasses, I'd also need a way for the ReportBuilder to accept instructions for irregularly displayed data (e.g. a separate totaled or averaged value).
* BeautifulSoup doesn't seem to like pages that are all links.



## Instructions

After downloading the code:
1. In your terminal, `cd` into `topsitessummarized`.
2. If you'd like to create a virtualenvironment, create one. Make sure to use `-p python3`.
2. `pip install -r requirements.txt` will install the requirements.
3. In your terminal, type `python main.py <email> <password>`, where email and password are used to access your valid Alexa account. If your default python installation is 2.7, make sure to type `python3` instead of `python`.

While the program runs it will provide feedback on its current status to stdout.


# Developer Instructions

If you'd like to use the ReportBuilder for building your own reports, you should subclass it. HeaderReportBuilder is a good example of a standard report. WordCountReportBuilder and PerformanceReportBuilder are examples of the ways you might override for custom data. I've already included some methods in ReportBuilder to assist with this.

SiteRetriever should be useful as an example of a way to retrieve data from a website and output it in a format that ReportBuilder will understand.
