from django.contrib.gis import admin
from models import *


#
# Search and visitors admin
#
class SearchAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('keywords')})
  field = (None, {'fields': ('geometry')})
  field = (None, {'fields': ('ip_position')})
  field = (None, {'fields': ('start_date')})
  field = (None, {'fields': ('end_date')})
  list_display = ('search_date', 'user', 'guid','start_date','end_date' )
  list_filter = ('search_date', 'user', )

class VisitAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('city')})
  field = (None, {'fields': ('country')})
  field = (None, {'fields': ('ip_address')})
  field = (None, {'fields': ('ip_position')})


class SacUserProfileAdmin (admin.GeoModelAdmin):
  list_display = ('user','strategic_partner' )
  list_filter = ('user','strategic_partner' )
  field = (None, {'fields': ('strategic_partner')})

class OrderStatusAdmin(admin.GeoModelAdmin):
  field = (None, {'fields': ('name')})

class OrderNotificationRecipientsAdmin(admin.GeoModelAdmin):
  list_display = ('user', )

  # This next method will filter the users list in the admin form
  # so that only staff members can be chosen from the users list
  def render_change_form(self, request, context, *args, **kwargs):
    context['adminform'].form.fields['user'].queryset = User.objects.filter(is_staff=True)
    return super(OrderNotificationRecipientsAdmin, self).render_change_form(request, context, args, kwargs)

#################################################
# Admin models for new generic product model
#################################################

class MissionAdmin( admin.GeoModelAdmin ):
  pass
class ProcessingLevelAdmin( admin.GeoModelAdmin ):
  pass
class DatumAdmin( admin.GeoModelAdmin ):
  pass
class InstitutionAdmin( admin.GeoModelAdmin ):
  pass
class LicenseAdmin( admin.GeoModelAdmin ):
  pass
class ProjectionAdmin( admin.GeoModelAdmin ):
  pass
class QualityAdmin( admin.GeoModelAdmin ):
  pass
class CreatingSoftwareAdmin( admin.GeoModelAdmin ):
  pass
class GenericProductAdmin( admin.GeoModelAdmin ):
  pass
class GeospatialProductAdmin( admin.GeoModelAdmin ):
  pass
class OpticalProductAdmin( admin.GeoModelAdmin ):
  list_filter = ('mission', 'mission_sensor', 'sensor_type', 'processing_level', 'product_acquisition_start' )
class ResamplingMethodAdmin( admin.GeoModelAdmin ):
  pass
class FileFormatAdmin( admin.GeoModelAdmin ):
  pass
class DeliveryMethodAdmin( admin.GeoModelAdmin ):
  pass
class OrderStatusAdmin( admin.GeoModelAdmin ):
  pass
class MissionSensorAdmin( admin.GeoModelAdmin ):
  pass
class TaskingRequestAdmin( admin.GeoModelAdmin ):
  pass
class SumbAdmin( admin.GeoModelAdmin ):
  pass

admin.site.register(Sumb, SumbAdmin)
admin.site.register(TaskingRequest, TaskingRequestAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(MissionSensor, MissionSensorAdmin)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(FileFormat, FileFormatAdmin)
admin.site.register(ResamplingMethod, ResamplingMethodAdmin)
admin.site.register(ProcessingLevel, ProcessingLevelAdmin)
admin.site.register(Datum, DatumAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Projection, ProjectionAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(CreatingSoftware, CreatingSoftwareAdmin)
admin.site.register(GenericProduct, GenericProductAdmin)
admin.site.register(OpticalProduct, OpticalProductAdmin)
admin.site.register(GeospatialProduct, GeospatialProductAdmin)
admin.site.register(OrderNotificationRecipients, OrderNotificationRecipientsAdmin)

#################################################
# End of admin models for new generic product model
#################################################

admin.site.register(Search, SearchAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(SacUserProfile, SacUserProfileAdmin)
