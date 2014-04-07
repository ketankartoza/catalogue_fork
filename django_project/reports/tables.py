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
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
import django_tables2 as tables
from catalogue.models import Visit

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


def render_user_names(record):
    """
    A helper function to return a string to represent a User in our tables

    :param record: The record which has a User FK relationship
    :return: user's name representation :rtype: str
    """
    if record.user:
        if record.user.first_name:
            return '%s %s' % (
                record.user.first_name,
                record.user.last_name or None
            )
        else:
            return record.user.username
    else:
        return 'No User Recorded'


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


class SANSADateColumn(tables.DateColumn):
    """
    A subsclass of tables.DateColumn to render a date Column in a consistent
    format
    """
    def render(self, value, **kwargs):
        """
        Render's the cell's value in the defined date format
        """
        return value.strftime('%a %d %b %Y')


class CountryTable(tables.Table):
    """
    Renders a Country/Count table
    """
    country = TitleColumn()
    count = tables.Column()


class SatelliteInstrumentTable(tables.Table):
    """
    Renders a SatelliteInstrumentTable
    """
    sensor = tables.Column(accessor='satellite.name')
    instrument_type = tables.Column(
        accessor='instrument_type.name',
        verbose_name='Instrument Type'
    )
    abbreviation = tables.Column(accessor='satellite.abbreviation')
    count = tables.Column(
        accessor='id__count',
        verbose_name='Search Count'
    )


class OrderListTable(tables.Table):
    """
    Renders an Orders table
    """
    id = tables.Column()
    order_date = SANSADateColumn()
    order_status = tables.Column()
    user = tables.Column()
    view = tables.URLColumn(
        empty_values=(),
        sortable=False,
        verbose_name='View Order'
    )

    def render_view(self, record):
        """
        We need to add HTML for a link to view the details of each Order
        object

        :param record: The Order object rendered in this row
        """
        return mark_safe(
            '<a href="/vieworder/%s/"><i class="icon-search"></i></a>'
            % record.id
        )


# noinspection PyMethodMayBeStatic
class SearchesTable(tables.Table):
    """
    Renders a table of Search objects
    """
    searched_by = tables.Column(empty_values=())
    search_date = SANSADateColumn()
    satellites = tables.Column(empty_values=())
    sensors = tables.Column(empty_values=())
    date_ranges = tables.Column(empty_values=())
    actions = tables.Column(empty_values=(), orderable=False)

    def render_searched_by(self, record):
        """
        We need to render the User's first and last names

        :param record: The SearchRecord being rendered
        :return: User's first_name and last_name
        :rtype: str
        """
        return render_user_names(record)

    def render_satellites(self, record):
        """
        Render a list of instrument types used in the search
    
        :param record: The SearchRecord object being rendered
        :return: satellite_string
        :rtype: str
        """
        satellites = record.satellites_as_list()
        if len(satellites) > 0:
            satellite_string = ', '.join(satellites)
        else:
            satellite_string = None
        return satellite_string

    def render_sensors(self, record):
        """
        Render a list of instrument types used in the search

        :param record: The SearchRecord object being rendered
        :return: sensor_string
        :rtype: str
        """
        sensors = record.sensors_as_list()
        if len(sensors) > 0:
            sensor_string = ', '.join(sensors)
        else:
            sensor_string = None
        return sensor_string

    def render_date_ranges(self, record):
        """
        We need to render record.dates_as_string in date_ranges column
        :param record: The SearchRecord object rendered in this row
        """
        return record.dates_as_string

    def render_actions(self, record):
        """
        Render the appropriate links for each record's action cell

        :param record: The object being rendered in this row
        :return: unescaped HTML :rtype: str
        """
        return mark_safe(
            '<a href="%(guid_url)s" class="view-btn">'
            '<i class="icon-search"></i></a> '
            '<a href="%(delete_url)s" '
            'onclick="%(delete_url)s?xhr\');'
            '$(this).parent().parent().remove();return false;\' '
            'class="remove-btn"><i class="icon-remove"></i></a>' % {
                'guid_url': reverse('searchGuid', args={record.guid}),
                'delete_url': reverse('deleteSearch', args={record.id})
            }
        )


class VisitorTable(tables.Table):
    """
    A table to render a list of Visitors
    """
    user = tables.Column(empty_values=())

    # noinspection PyMethodMayBeStatic
    def render_user(self, record):
        """
        Render the user's name representation

        :param record: The record being rendered in this row
        :return: User's name representation :rtype: str
        """
        return render_user_names(record)

    class Meta(object):
        """
        Adding CSS classes to the table (required for Bootstrap) and setting
        other Meta attributes
        """
        model = Visit
        exclude = ('ip_position', 'id')
        sequence = (
            'user', 'ip_address', 'country', 'city', 'visit_date'
        )
