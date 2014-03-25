# coding=utf-8
"""
SANSA-EO Catalogue - Report application tables and table-helpers

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""
import django_tables2 as tables

__author__ = 'george@grvhi.com'
__version__ = '0.1'
__date__ = '17/08/2012'
__copyright__ = 'South African National Space Agency'


def table_sort_settings(request):
    """
    Helper function to fetch sort and order from GET and set the consequent
    value for sort_link which is appended to the table sort links in the
    template

    :param request: HttpRequest
    :return: sort_col, sort_order, sort_link :rtype: str
    """
    sort_col = request.GET.get('sort', None)
    sort_order = request.GET.get('order', None)
    if sort_order == 'ASC':
        sort_link = 'DESC'
    elif sort_order == 'DESC':
        sort_link = 'ASC'
    else:
        sort_link = 'DESC'
    return sort_col, sort_order, sort_link


class TitleColumn(tables.Column):
    """
    Returns a column with a titled cell value
    (i.e. "South Africa", not "south africa")
    """
    def render(self, value):
        """
        Renders the cell's value
        :param value: cell value
        :return: value.title() :rtype: str
        """
        return value.title()


class CountryTable(tables.Table):
    """
    Renders a County/Count table
    """
    country = TitleColumn()
    count = tables.Column()

    class Meta(object):
        """
        Adding CSS class attrs to the table (required for Bootstrap)
        """
        attrs = {
            'class': 'table table-striped'
        }