from abc import ABCMeta, abstractmethod

class BaseReportBuilder(metaclass=ABCMeta):
    """
    Base class for report builders.
    """

    def __init__(self, data, categories):
        self.data = data
        self.categories = categories

    @abstractmethod
    def create_report(self):
        pass

    @abstractmethod
    def build_report(self):
        pass

    @abstractmethod
    def build_table(self):
        pass


# what changes:
# categories, header, unique rows (linked to categories), report format (html, css etc)
# what stays the same:
# building and creating a report, building a table

# make categories an input to __init__
# make unique rows some sort of mixin. It needs to override build_table
# For each row, I need the type of calculation and the category name.
# I'll also need to have different implementations for different report formats.
# Maybe specify format as well, or store format as a ReportBuilder attribute
# and grab that, so it's not user specified.

class NonStandardRowMixin:
    """
    Used to add a nonstandard row to a report.
    """
    pass

class ReportBuilder(BaseReportBuilder):
    """
    Basic class for building an html report.
    """
    def __init__(self, data):
        """
        data: a list of dictionaries used to populate rows in the report.
        """
        self.data = data
        self.categories = []
        # The header value is used for generating a report title and header.
        self.header = "Report"

    def create_report(self, file_format):
        """
        Create an html report.
        """
        report = self.build_report()
        filename = "{0}.{1}".format(self.header, file_format)
        with open(filename, "w") as f:
            f.write(report)

    def build_report(self):
        """
        Return an html report.
        """
        headings =\
        """
        <head>
            <title>{0}</title>
        </head>
        <body>
        <h2>{0}</h2><br>
        """.format(self.header)

        table = self.build_table()
        report = "{0}{1}<br><br><br></body>".format(headings, table)
        return report

    def build_table(self):
        """
        Return an html table.

        The ReportBuilder categories
        are used for data retrieval and table header creation.
        """
        table = ""
        table_header = self._build_table_header()
        table += table_header
        for index, site_dict in enumerate(self.data, 1):
            unfinished_row = self._build_site_row(site_dict)
            row = "<tr><td>{0}</td>{1}</tr>".format(index, unfinished_row)
            table += row
        table = "<table border=\"1\">{0}</table>".format(table)
        return table

    def _build_table_header(self):
        """
        Return an html table header.
        """
        table_header = ""
        for category in self.categories:
            pretty_category = self._prettify_variable_name(category)
            table_header += "<th>{0}</th>".format(pretty_category)
        table_header = "<tr><th>Ranking</th>{0}</tr>".format(table_header)
        return table_header

    def _prettify_variable_name(self, variable_name):
        """
        Return a python variable with underscore replaced by a space.
        """
        return variable_name.replace("_", " ")

    def _build_site_row(self, site_dict):
        """
        Return an html table row
        containing data for all of the predefined categories.
        """
        site_row = ""
        for category in self.categories:
            category_value = site_dict[category]

            if isinstance(category_value, list):
                category_value = ", ".join(sorted(category_value))

            category_html = """
                            <td>{0}</td>
                            """.format(category_value)
            site_row += category_html
        return site_row

    def _get_average(self, some_list):
        """
        Return the average of all values in a list.
        """
        return sum(some_list) / len(some_list)

    def _get_sum(self, some_list):
        """
        Return the sum of all values in a list.
        """
        return sum(some_list)

    def _update_list(self, current_category, sought_category,
                          list_to_update, value):
        """
        If the current category matches the sought_category parameter,
        update the associated instance list attribute.

        This is useful when values are being stored
        for later processing/consumption.

        current_category: the category being checked.
        sought_category: the category that current_category must match.
        list_to_update: the list to which a value will be added.
        value: the value to be added.
        """
        if current_category == sought_category:
            list_to_update.append(float(value))

    def _remove_closing_table_tag(self, table):
        """
        Return a table with the closing tag removed.

        This is useful for subclasses
        that add non-standard rows to the table.
        """
        return table[:-8]

    def _build_reduce_row(self, method_applied, category_name, reduced_value):
        """
        Return a row formatted to display a single value.

        Any time that a list is reduced,
        this method can be used to generate a row for the value.
        method_applied: the name of the method e.g. average or total.
        category_name: the category of the data.
        reduced_value: the value to be displayed.
        """
        average_row = """<tr>
                        <td><b>{0} {1}:</b></td>
                        <td><b>{2}</b></td>
                        </tr>""".format(method_applied,
                                        category_name,
                                        reduced_value)
        return average_row


class WordCountReportBuilder(ReportBuilder):
    """
    Used to build a Word Count report.
    """
    def __init__(self, data):
        super().__init__(data)
        self.categories = ["site_name", "word_count"]
        self.word_counts = []
        self.header = "Word Count Report"

    def build_table(self):
        """
        Return a table of data.

        This subclass adds a row for average word count.
        """
        table = super().build_table()
        table = self._remove_closing_table_tag(table)
        average_word_count = self._get_average(self.word_counts)
        average_word_count_row = self._build_reduce_row("average", "word count",
                                                         average_word_count)
        table += average_word_count_row
        table += "</table>"
        return table

    def _build_site_row(self, site_dict):
        """
        Return a row containing data for all of the predefined categories.
        """
        site_row = ""
        for category in self.categories:
            category_value = site_dict[category]

            if isinstance(category_value, list):
                category_value = ", ".join(sorted(category_value))

            category_html = """
                            <td>{0}</td>
                            """.format(category_value)
            site_row += category_html
            self._update_list(category, "word_count",
                           self.word_counts, category_value)
        return site_row


class HeaderReportBuilder(ReportBuilder):
    """
    Used to build a Header report.
    """

    def __init__(self, data):
        super().__init__(data)
        self.categories = ["site_name", "headers", "cookies"]
        self.header = "Header Report"


class PerformanceReportBuilder(ReportBuilder):
    """
    Used to build a Performance report.
    """
    def __init__(self, data):
        super().__init__(data)
        self.categories = ["site_name", "time_to_complete"]
        self.header = "Performance Report"
        self.performance_counts = []

    def build_table(self):
        """
        Return a table of data.

        This subclass adds a row for average word count.
        """
        table = super().build_table()
        # I can get an add_row method from the mixin that does the following.
        table = self._remove_closing_table_tag(table)
        total_time = self._get_sum(self.performance_counts)
        total_performance_row = self._build_reduce_row("total", "time",
                                                       total_time)
        table += total_performance_row
        table += "</table>"
        return table

    def _build_site_row(self, site_dict):
        """
        Return a row containing data for all of the predefined categories.
        """
        site_row = ""
        for category in self.categories:
            category_value = site_dict[category]

            if isinstance(category_value, list):
                category_value = ", ".join(sorted(category_value))

            category_html = """
                            <td>{0}</td>
                            """.format(category_value)
            site_row += category_html
            # update list would also go into the mixin, and everything above
            # is covered by a call to super().
            self._update_list(category, "time_to_complete",
                           self.performance_counts, category_value)
        return site_row
