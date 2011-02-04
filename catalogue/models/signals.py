# for product_date soft trigger
from django.db import models
from products import OpticalProduct, RadarProduct
import datetime

def set_generic_product_date(sender, instance, **kw):
  """
  Sets the product_date based on acquisition date,
  if both start_date and end_date are set, then calculate the avg,
  uses the start_date if end_date is not set
  """
  if instance.product_acquisition_end:
    instance.product_date = datetime.datetime.fromordinal(instance.product_acquisition_start.toordinal() \
        + (instance.product_acquisition_end - instance.product_acquisition_start).days)
  else:
    instance.product_date = instance.product_acquisition_start
  logging.info('Pre-save signal activated for %s' % instance)


# ABP: doesn't work for GenericSensorProduct: need the child models :(
models.signals.pre_save.connect(set_generic_product_date, sender = OpticalProduct)
models.signals.pre_save.connect(set_generic_product_date, sender = RadarProduct)

