### Description
This program collects the names of the top 100 sites on Alexa.

It accesses each of the top 100 sites on Alexa, collecting:
* the total word count of the site's landing page,
* the site's header names and
* the site's cookie names.

For each site, the script tracks how long it took to access the page and gather data.

It outputs three HTML reports in table format:
* A report of word count by site, including an average of all sites.
* A report of alphabetized headers and cookies by site.
* A report of site access time and the total time to access all sites.

### Instructions
After downloading the code:

1.  In your terminal, `cd` into `retrievegeneratereport`.

2.  If you'd like to create a virtualenvironment, create one with `virtualenv -p python3 env`. (Activate it with `source env/bin/activate`).

3.  `pip install -r requirements.txt` will install the requirements.

4.  In your terminal, type `python main.py <email> <password>`, where `email` and `password` are used to access your valid Alexa account. If your default python installation is 2.7 and you aren't using a virtual environment, make sure to type `python3` instead of `python`.

5.  You can run the unit tests with `python tests.py`.

While the program runs it will provide feedback on its current status to stdout.

Once it has finished, it will produce the three reports as html files in the same directory.


### Potential Enhancements and Improvements
* Get better test coverage.
* Find the most common cookie and header names, excluding the most typical headers.
* Use a Counter from collections to track header and cookie name frequency. Display a frequency report.
* Detect the language for each site.
* Generate a score based on the ratio of words to ranking.
* Generate a score based on the ratio of ranking to performance.
* Abstract the SiteRetriever and ListingsRetriever classes a bit, and create a base class for each of them to inherit from. This would allow a more consistent interface for generating data that a subclass of ReportBuilder could consume.
* ~~I might consider abstracting out the categories used for column creation, but in order for that to be an effective way to reduce the need for subclasses, I'd also need a way for the ReportBuilder to accept instructions for irregularly displayed data (e.g. a separate totaled or averaged value).~~ Completed for v0.2!

### Developer Instructions/Notes

If you'd like to use the ReportBuilder for building your own reports, you can instantiate it. To build reports that summarize or average the values of a field, instantiate CustomRowReportBuilder. See their docstrings, and the docstring of NonStandardRowMixin, for more information.

HeaderReportBuilder is a good example of a standard report. WordCountReportBuilder and PerformanceReportBuilder are examples of nonstandard reports. These are only included for backwards compatibility. Subclassing shouldn't be necessary for the above use cases.

SiteRetriever is an example of a way to retrieve data from a website and output it in a format that ReportBuilder will understand.

timer.py has a useful wrapper for timing tasks. It's almost exactly what the Python Cookbook suggests, but I modified it to add the value to the dictionary returned by the method. Note: this will only work if the method returns a dictionary.

#### Update notes for v0.2
Still need to improve the documentation, update tests and make a pass to tidy up variable names. Major changes are as follows:
* New abstract base class: BaseReportBuilder
* New mixin: NonStandardRowMixin. Use for appending a field that averages or sums a column.
* Improved extensibility: report format is provided as an argument. Currently only supports html reports.
* Backwards Compatibility! The boilerplate builder classes now implement the new functionality, reducing the need for a complete rewrite of code that depended on the old builders.
