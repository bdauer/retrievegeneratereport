from abc import ABCMeta, abstractmethod

class BaseReportBuilder(metaclass=ABCMeta):
    """
    Base class for report builders.
    """
    def __init__(self, header, categories, data):
        self.data = data
        self.categories = categories

    @abstractmethod
    def create_report(self):
        pass

    @abstractmethod
    def build_report(self):
        pass

class NonStandardRowMixin:
    """
    Used to add a nonstandard row to a report.

    Currently the only nonstandard functionality is to reduce a column,
    specifically one that has been averaged or summed.

    The NonStandardRowMixin has an additional required keyword argument:
    _reduced_columns.
    The value should be a list of dictionaries in the following format:
    {"column_name": this should be the name of the column,
      "method": sum or average,
      "value": []}

    Two cells will be appended to the table for each of the dictionaries.
    The first cell describes gives the method and column name.
    The second cell gives the new value.
    """
    def __init__(self, *args, _reduced_columns, **kwargs):
        self._reduced_columns = _reduced_columns
        super().__init__(*args, **kwargs)

    def _update_list(self, current_category, value):
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
        for category_data in self._reduced_columns:
            if current_category == category_data["column_name"]:
                category_data["value"].append(float(value))

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
        reduced_row = """<tr>
                        <td><b>{0} {1}:</b></td>
                        <td><b>{2}</b></td>
                        </tr>""".format(method_applied,
                                        category_name,
                                        reduced_value)
        return reduced_row

    def build_html_table(self):
        """
        Return a table of data.
        This subclass adds a row for average word count.
        """
        table = super().build_html_table()
        # I can get an add_row method from the mixin that does the following.
        table = self._remove_closing_table_tag(table)

        for special_column_data in self._reduced_columns:
            for site_dict in self.data:
                category = special_column_data["column_name"]
                if category == site_dict["site_name"]:
                    self._build_column_data(category, site_dict)

            method = special_column_data["method"]
            value = special_column_data["value"]
            if method == "sum":
                pretty_method = "total"
                reduced_value = self._get_sum(value)
            elif special_column_data["method"] == "average":
                pretty_method = "avg"
                reduced_value = self._get_average(value)
            reduced_row = self._build_reduce_row(pretty_method, category,
                                                       reduced_value)
            table += reduced_row
        table += "</table>"
        return table

    def _build_column_data(self, category, site_dict):
        """
        Return formatted data for a column.

        category: a column name.
        site_dict: a dict representing the data gathered from a site.
        """
        column_data = super()._build_column_data(
                                category, site_dict)
        category_value = site_dict[category]
        self._update_list(category, category_value)
        return column_data

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

class ReportBuilder(BaseReportBuilder):
    """
    Basic class for building an html report.
    """
    def __init__(self, header, categories, data):
        """
        data: a list of dictionaries used to populate rows in the report.
        """
        self.data = data
        self.categories = categories
        # The header value is used for generating a report title and header.
        # self.header = "Report"
        self.header = header

    def create_report(self, file_format):
        """
        Create an html report.
        """
        report = self.build_report(file_format)
        filename = "{0}.{1}".format(self.header, file_format)
        with open(filename, "w") as f:
            f.write(report)

    def build_report(self, file_format):
        """
        Build a report in the requested file format.

        file_format: The format to use for the file.
        Currently supports html.

        This method delegates to a build method appropriate to the provided
        file_format.
        """
        if file_format == "html":
            report = self.build_html_report()
        return report

    def build_html_report(self):
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

        table = self.build_html_table()
        report = "{0}{1}<br><br><br></body>".format(headings, table)
        return report

    def build_html_table(self):
        """
        Return an html table.

        The ReportBuilder categories
        are used for data retrieval and table header creation.
        """
        table = ""
        table_header = self._build_html_table_header()
        table += table_header
        for index, site_dict in enumerate(self.data, 1):
            unfinished_row = self._build_site_row(site_dict)
            row = "<tr><td>{0}</td>{1}</tr>".format(index, unfinished_row)
            table += row
        table = "<table border=\"1\">{0}</table>".format(table)
        return table

    def _build_html_table_header(self):
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
            site_row += self._build_column_data(category, site_dict)
        return site_row

    def _build_column_data(self, category, site_dict):
        """
        Return formatted data for a column.

        category: a column data category.
        site_dict: a dict representing the data gathered from a site.
        """
        category_value = site_dict[category]

        if isinstance(category_value, list):
            category_value = ", ".join(sorted(category_value))

        category_html = """
                        <td>{0}</td>
                        """.format(category_value)
        return category_html

class CustomRowReportBuilder(NonStandardRowMixin, ReportBuilder):
    """
    Use this class when adding a special row.
    """
    pass

class WordCountReportBuilder(CustomRowReportBuilder):
    """
    Used to build a Word Count report.
    """
    def __init__(self, data):
        self.categories = ["site_name", "word_count"]
        reduced_columns = [{"column_name": "word_count",
                           "method": "average",
                           "value": []}]
        self.header = "Word Count Report"
        super().__init__(
            self.header, self.categories, data, _reduced_columns=reduced_columns)

class HeaderReportBuilder(ReportBuilder):
    """
    Used to build a Header report.
    """
    def __init__(self, data):
        self.categories = ["site_name", "headers", "cookies"]
        self.header = "Header Report"
        super().__init__(self.header, self.categories, data)


class PerformanceReportBuilder(CustomRowReportBuilder):
    """
    Used to build a Performance report.
    """
    def __init__(self, data):
        self.categories = ["site_name", "time_to_complete"]
        self.header = "Performance Report"
        reduced_columns = [{"column_name": "word_count",
                           "method": "sum",
                           "value": []}]
        super().__init__(
            self.header, self.categories, data, _reduced_columns=reduced_columns)
