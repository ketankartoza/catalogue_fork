import logging
logger = logging.getLogger(__name__)
from webodt.shortcuts import render_to
from catalogue.models import (
    Order,
    OrderStatusHistory,
    OrderNotificationRecipients,
)
from search.models import SearchRecord


def generateOrderPDF(theUser, theOrderID):
    """
    myOrderID: The ID of the order requesting a PDF
    return: Should return a file object which can be attached to an email in
    catalogue.views.orders.notifySalesStaff
    """
    logger.info('PDF Order Summary requested for order ID: %s' % theOrderID)
    try:
        myOrder = Order.objects.get(Order, id=theOrderID)
    except Order.DoesNotExist:
        myOrder = None
        logger.info('PDF Order Summary failed. Order ID (%s) not found' %
                    theOrderID)
        return TypeError('The provided order ID could not be found')
    myRecords = SearchRecord.objects.filter(user=theUser,
                                            order=myOrder).select_related()
    myHistory = OrderStatusHistory.objects.filter(order=myOrder)
    context = {'myOrder': myOrder,
               'myRecords': myRecords,
               'myHistory': myHistory}
    return render_to('order-summary.odt',
                     dictionary=context, format='pdf',
                     filename='Order Summary %s.pdf' % theOrderID,
                     delete_on_close=True
                     )
