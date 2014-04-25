from django.conf.urls import patterns, url

from .views import (
    myOrders,
    list_orders,
    order_monthly_report,
    downloadOrder,
    downloadClipGeometry,
    downloadOrderMetadata,
    viewOrder,
    updateOrderHistory,
    addOrder,
    ordersSummary,
    addAdhocOrder,
    convertPrice
)
# Here are our patterns
urlpatterns = patterns(
    '',
    url(r'^addorder/', addOrder, name='addOrder'),
    url(r'^downloadclipgeometry/(?P<theId>\d*)/$',
        downloadClipGeometry, name='downloadClipGeometry'),
    url(r'^downloadordermetadata/(?P<theId>\d*)/$',
        downloadOrderMetadata, name='downloadOrderMetadata'),
    url(r'^downloadorder/(?P<theId>\d*)/$',
        downloadOrder, name='downloadOrder'),
    url(r'^myorders/$', myOrders, name='myOrders'),
    url(r'^listorders/$', list_orders, name='listOrders'),
    url(r'^ordermonthlyreport/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        order_monthly_report, name='orderMonthlyReport'),
    url(r'^vieworder/(?P<theId>[0-9]+)/$', viewOrder, name='viewOrder'),
    url(r'^updateorderhistory/$',
        updateOrderHistory, name='updateOrderHistory'),
    url(r'^orderssummary/$', ordersSummary, name='ordersSummary'),
    url(r'^addadhocorder/', addAdhocOrder, name='addAdhocOrder'),
    url(r'^convertprice/', convertPrice, name='convertPrice'),
)
