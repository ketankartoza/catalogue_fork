from django.conf.urls import patterns, url

from .views import (
    search_history,
    recent_searches,
    search_monthly_report,
    searchMonthlyReportAOI,
    visitor_list,
    visitor_report,
    visitor_monthly_report,
    data_summary_table,
    dictionaryReport,
    sensorSummaryTable,
)


urlpatterns = patterns(
    '',
    url(r'^mysearches/$', search_history, name='searchHistory'),
    url(r'^recentsearches/$', recent_searches, name='recentSearches'),
    url(r'^searchmonthlyreport/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        search_monthly_report, name='searchMonthlyReport'
        ),
    url(r'^searchmonthlyreportaoi/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$',
        searchMonthlyReportAOI, name='searchMonthlyReportAOI'
        ),
    url(r'^visitorlist/$', visitor_list, name='visitorList'),
    url(r'^visitorreport/$', visitor_report, name='visitorReport'),
    url(r'^visitormonthlyreport/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        visitor_monthly_report, name='visitorMonthlyReport'
        ),
    url(r'^dataSummaryTable/$', data_summary_table, name='dataSummaryTable'),
    url(r'^dictionaryReport/$', dictionaryReport, name='dictionaryReport'),
    url(r'^sensorSummaryTable/(?P<theSensorId>[0-9]+)/$',
        sensorSummaryTable, name='sensorSummaryTable'
        ),
)
