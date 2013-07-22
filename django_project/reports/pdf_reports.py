import logging
logger = logging.getLogger(__name__)
from webodt.shortcuts import render_to


def generatePDF(template=None,
                theOrderID=None,
                context=None,
                pdfType=None):
    """
    myOrderID: The ID of the order requesting a PDF
    return: Should return a file object which can be attached to an email in
    catalogue.views.helpers.notifySalesStaff
    """
    logger.info('PDF requested for %s. ID: %s' % (pdfType, theOrderID))
    return render_to(template_name=template,
                     dictionary=context,
                     format='pdf',
                     delete_on_close=True
                     )
