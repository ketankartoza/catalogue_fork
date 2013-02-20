"""
SANSA-EO Catalogue - Catalogue forms

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

import datetime
import time

from django import forms
from django.forms.models import BaseInlineFormSet
#from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
#from django.core.validators import EMPTY_VALUES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Button,
    Div,
    Tab,
    TabHolder,
    HTML,
    Field
)
from crispy_forms.bootstrap import (
    FormActions
)

from catalogue.fields import (
    IntegersCSVIntervalsField,
    NoValidationChoiceField,
    AbbreviationModelChoiceField)

from catalogue.models import (
    RadarProduct,
    AcquisitionMode,
    MissionSensor,
    Mission,
    SensorType,
    ProcessingLevel,
)

from .models import (
    Search,
    SearchDateRange,
)
# from catalogue.models import (
#     RadarProduct,
#     MissionSensor,
#     Search,
#     AcquisitionMode,
#     Mission,
#     SensorType,
#     ProcessingLevel,
#     SearchDateRange,
#     OrderStatus,
#     Order,
#     Projection,
#     DeliveryDetail,
#     SearchRecord,
#     TaskingRequest,
#     OrderStatusHistory,
#     Clip)

from catalogue.datetimewidget import DateTimeWidget
from catalogue.aoigeometry import AOIGeometryField

# Support dmy formats (see
#    http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
    '%d-%m-%Y',               # '25-10-2005'
    '%d/%m/%Y', '%d/%m/%y',   # '25/10/2006', '25/12/06'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
)


class DateRangeFormSet(BaseInlineFormSet):
    """
    Date range search formsets with validation

    This class needs some override to handle the case of
    missing (deleted) forms.

    """
    def clean(self):
        """
        Delete incomplete forms
        TODO: simplify overlapping ranges (or raise exception), priority: low
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on
            # its own
            return
        empty_forms = []
        for i in range(0, len(self.forms)):
            form = self.forms[i]
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            # Checks for empty forms
            if not(start_date and end_date) or self._should_delete_form(form):
                empty_forms.append(i)
            elif start_date > end_date:
                raise forms.ValidationError, (
                    'Start date must be before or equal to end date.')
        # Delete empty/deleted forms
        empty_forms.reverse()
        for i in empty_forms:
            del(self.forms[i])
        self.management_form.cleaned_data['TOTAL_FORMS'] = len(self.forms)
        if not len(self.forms):
            raise forms.ValidationError, 'At least one date range is required.'
        #Next line disabled as it causes a crash
        #logging.debug('Date range forms:', self.forms)

    def is_valid(self):
        """
        Returns True if form.errors is empty for every form in self.forms.
        ABP: changed the range to len(self.forms)
        """
        if not self.is_bound:
            return False
        # We loop over every form.errors here rather than short circuiting on
        # the first failure to make sure validation gets triggered for every
        # form.
        forms_valid = True
        # err = self.errors
        for i in range(0, len(self.forms)):
            form = self.forms[i]
            if self.can_delete:
                if self._should_delete_form(form):
                    # This form is going to be deleted so any of its errors
                    # should not cause the entire formset to be invalid.
                    continue
            if bool(self.errors[i]):
                forms_valid = False
        return forms_valid and not bool(self.non_form_errors())

    def full_clean(self):
        """
        Cleans all of self.data and populates self._errors.
        ABP: changed the range to len(self.forms)
        """
        self._errors = []
        if not self.is_bound:  # Stop further processing.
            return
        for i in range(0, len(self.forms)):
            form = self.forms[i]
            self._errors.append(form.errors)
        # Give self.clean() a chance to do cross-form validation.
        try:
            self.clean()
        except ValidationError, e:
            self._non_form_errors = self.error_class(e.messages)


class AdvancedSearchForm(forms.ModelForm):
    """
    Let the user perform searches on sensors, by date and/or geometry
    digitised on map.
    """
    # keywords = forms.CharField(widget=forms.TextInput(
    #    attrs={'cols':'32'}),required=False)
    # Note1: the help_text strings are duplicated from the model help text
    #        since I didnt find a simple way to reuse it if adding custom
    #        fields
    # Note2: Only custom fields are added here. Fields that need no tweaking
    #        are pulled by the form generator directly from the model

    POLARISING_MODE_CHOICES = {'': 'All'}
    POLARISING_MODE_CHOICES.update(dict(RadarProduct.POLARISING_MODE_CHOICES))
    # ABP: the common part: will be searched on GenericProducts class only
    start_datepicker = forms.DateField(
        widget=DateTimeWidget(
            attrs={
                'title': 'Choose the start date for this date range.',
                'data-date_focus': 'start'}),
        required=False, label='Start date', input_formats=DATE_FORMATS,
        error_messages={
            'required': 'Entering a start date for your search is required.'},
        help_text='Start date is required. DD-MM-YYYY.')
    end_datepicker = forms.DateField(
        widget=DateTimeWidget(
            attrs={
                'title': 'Choose the end date for this date range.',
                'data-date_focus': 'end'}),
        required=False, label='End date', input_formats=DATE_FORMATS,
        error_messages={
            'required': 'Entering an end date for your search is required.'},
        help_text='End date is required. DD-MM-YYYY.')
    geometry = forms.CharField(
        widget=forms.HiddenInput(), required=False,
        help_text=(
            'Digitising an area of interest is not required but is recommended'
            '. You can use the help tab in the map area for more information '
            'on how to use the map. Draw an area of interest on the map to '
            'refine the set of search results to a specific area.'))

    geometry_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'file'}),
        required=False,
        help_text=(
            'Upload a zipped shapefile or KML/KMZ file of less than 1MB. If '
            'the shapefile contains more than one polygon, only the first will'
            ' be used. Complex polygons will increase search time.'))

    isAdvanced = forms.CharField(widget=forms.HiddenInput(), required=False)
    polarising_mode = forms.ChoiceField(
        choices=tuple(POLARISING_MODE_CHOICES.viewitems()), required=False)
    geometry = forms.CharField(
        widget=forms.HiddenInput(), required=False,
        help_text=(
            'Digitising an area of interest is not required but is recommended'
            '. You can use the help tab in the map area for more information '
            'on how to use the map. Draw an area of interest on the map to '
            'refine the set of search results to a specific area.'))
    aoi_geometry = AOIGeometryField(
        widget=forms.TextInput(attrs={'title': (
            'Enter bounding box coordinates separated by comma for Upper '
            'left and Lower right coordinates i.e. (20,-32,22,-34), or '
            'enter single coordinate which defines circle center and '
            'radius in kilometers (20,-32,100). Alternatively, digitise '
            'the clip area in the map.')
        }),
        required=False)

    k_orbit_path = IntegersCSVIntervalsField(
        required=False,
        help_text=(
            'Insert the orbit path as a list of comma separated values or '
            'ranges (e.g. : "10,20,30" or  "20-40")'))
    j_frame_row = IntegersCSVIntervalsField(
        required=False,
        help_text=(
            'Insert the frame row as a list of comma separated values or '
            'ranges (e.g. : "10,20,30" or "20-40")'))
    # exclude PRODUCT_SEARCH_GENERIC from Search.PRODUCT_SEARCH_TYPES
    search_type = forms.ChoiceField(
        choices=Search.PRODUCT_SEARCH_TYPES[1:], required=False)
    cloud_mean = forms.IntegerField(
        min_value=0, max_value=100, initial=0,
        help_text=(
            'Select the maximum cloud cover (range 0-100) when searching for '
            'images. Note that not all sensors support cloud cover filtering.')
    )

    class Meta:
        model = Search
        exclude = (
            'ip_position', 'guid', 'keywords', 'geometry_file', 'user',
            'deleted', 'processing_level')

    # add Media class for this form, rendered specific for this form
    class Media:
        js = (
            "/media/js/widget.sansa-datepicker.js",
            "/media/js/widget.sansa-daterangecontainer.js",)

    def __init__(self, *args, **kwargs):
        """
        We are using jquery tooltip to show a nice tooltip for each field. To
        ensure that each field has a title set (which is used for the tooltip
        text), this function iterates the fields of a form and sets their
        title text to the help text for that field. If the title is already
        set, its left as is.
        """

        self.helper = FormHelper()
        self.helper.form_class = 'span12 form-horizontal gap-top'
        self.helper.form_id = 'search_form'
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.form_action = reverse('search', kwargs={})

        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Product type details:',
                    Div(
                        Field('search_type', template='myField.html'),
                        css_class="span5"
                    ),
                    Div(
                        Field('license_type', template='myField.html'),
                        css_class="offset1 span5"
                    ),
                    data_search_type='adv'
                ),
                Fieldset(
                    'Sensors:',
                    Div(
                        Field('sensors', template='myField.html'),
                        css_class="span5"
                    ),
                    Div(
                        Field('mission', template='myField.html'),
                        Field('sensor_type', template='myField.html'),
                        Field('acquisition_mode', template='myField.html'),
                        css_class="offset1 span5"
                    )
                ),
                Fieldset(
                    'Image details:',
                    Div(
                        Field('use_cloud_cover', template='myField.html'),
                        Field('sensor_inclination_angle_start', template='myField.html'),
                        Field('spatial_resolution', template='myField.html'),
                        css_class="span5"
                    ),
                    Div(
                        Field('cloud_mean', template='myField.html'),
                        Field('sensor_inclination_angle_end', template='myField.html'),
                        Field('band_count', template='myField.html'),
                        css_class="offset1 span5"
                    ),
                    data_search_type='adv'
                ),
                Fieldset(
                    'Row & path:',
                    Div(
                        Field('k_orbit_path', template='myField.html'),
                        css_class="span5"
                    ),
                    Div(
                        Field('j_frame_row', template='myField.html'),
                        css_class="offset1 span5"
                    ),
                    data_search_type='adv'
                ),
                Fieldset(
                    'Geometry:',
                    Div(
                        Field('aoi_geometry', template='myField.html'),
                        css_class="span5"
                    ),
                    Div(
                        Field('geometry_file', template='myField.html'),
                        css_class="offset1 span5"
                    ),
                    data_search_type='adv'
                ),
                Fieldset(
                    'Dates:',
                    Div(
                        Field('start_datepicker', template='myField.html'),
                        Field('end_datepicker', template='myField.html'),
                        css_class="span5"
                    ),
                    Div(
                        HTML('<a id="dr_add" title="Select the dates in the calendar and click here to add to the list." href="javascript:void(0)"><img src="/media/images/selector-add.gif"></a><br />'),
                        HTML('<a id="dr_del" title="Select the ranges in the list and click here to remove." href="javascript:void(0)"><img src="/media/images/selector-remove.gif"></a>'),
                        css_class="span1"
                    ),
                    Div(
                        HTML('<label for="id_searchdaterange_set">Date range *</label>'),
                        HTML('{{ myFormset.management_form }}'),
                        Div(
                            HTML('{% for form in myFormset.forms %}<div class="dr_row"><div class="dr_input">{{ form }}</div><div class="dr_text" title="Click to select."></div></div>{% endfor %}'),
                            id="dr_container",
                            css_class="well well-small"
                        ),
                        css_class="span5"
                    )
                ),
                css_class="span11"
            ),
            'geometry'
        )
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)
        # define smmple search form fields
        SIMPLE_FORM_FIELDS = ['sensors', 'start_datepicker', 'end_datepicker']
        for myFieldName, myField in self.fields.items():
            # Simple way to assign css class to every field
            if myFieldName not in SIMPLE_FORM_FIELDS:
                myField.widget.attrs['data-search-type'] = 'adv'
            myField.widget.attrs['class'] = 'ui-corner-all'
            if (not 'title' in myField.widget.attrs or
                    myField.widget.attrs['title'] == ''):
                myField.widget.attrs['title'] = myField.help_text

        self.fields['sensors'].required = True
        # Do not list empty dictionary items (avoid null searches)
        qs = AcquisitionMode.objects.order_by()
        self.fields['sensors'].queryset = (MissionSensor.objects
            .filter(pk__in=qs.distinct().values_list(
                'sensor_type__mission_sensor', flat=True))
            .filter(has_data=True)
            .order_by('name'))
        self.fields['mission'].queryset = (Mission.objects
            .filter(pk__in=qs.distinct().values_list(
                'sensor_type__mission_sensor__mission', flat=True))
            .filter(missionsensor__has_data=True))

    def clean_guid(self):
        """Custom validator for guid"""
        myCleanedData = self.cleaned_data
        myGuid = myCleanedData.get('guid')
        if not myGuid:
            myGuid = 'null'
            # we dont raise an error as we will just generate the guid in the
            # model's save method
        return myGuid

    def clean_ip_position(self):
        myCleanedData = self.cleaned_data
        myPoint = myCleanedData.get('ip_position')
        if not myPoint:
            myPoint = 'SRID=4326;POINT(0 0)'
        return myPoint

    def clean_end_date(self):
        """End date validator"""
        #Note that required=False fields are not passed to cleaned_data but
        #rather just to self.data
        myData = self.data
        myEndDate = myData.get('end_date')
        if not myEndDate:
            # date is empty which is ok so do nothing
            pass
        else:
            try:
                myEndDate = datetime.datetime(
                    *time.strptime(myEndDate, "%d-%m-%Y")[:6]).date()
            except:
                raise forms.ValidationError('End date was not valid.')
            #pass
        return myEndDate

    def clean(self):
        myCleanedData = self.cleaned_data
        logging.info('cleaned data: ' + str(myCleanedData))
        # ABP: checks for advanced search only (not in cleaned_data because it
        # does not belong to Search model)
        if self.data.get('isAdvanced') == 'true':
            # ABP: disabled because the DB has NULL in all rows
            # if not myCleanedData.get('geometric_accuracy_mean'):
                #self._errors["geometric_accuracy_mean"] = self.error_class([
                #"Error: Spatial resolution is required for advanced search!"])
                #raise forms.ValidationError(
                #    'Error: One or more required values are missing!')
            myStartSensorAngle = myCleanedData.get(
                'sensor_inclination_angle_start')
            myEndSensorAngle = myCleanedData.get(
                'sensor_inclination_angle_end')
            if ((myStartSensorAngle and myEndSensorAngle) and
                    (myEndSensorAngle < myStartSensorAngle)):
                self._errors['sensor_inclination_angle_start'] = (
                    self.error_class(['Check values.']))
                self._errors['sensor_inclination_angle_end'] = (
                    self.error_class(['Check values.']))
                raise forms.ValidationError(
                    'Error: Start sensor angle can not be greater than the end'
                    ' sensor angle!')
        # check if user selected sensors for search
        if (int(myCleanedData.get('search_type')) in (
                Search.PRODUCT_SEARCH_OPTICAL, Search.PRODUCT_SEARCH_RADAR)
                and not myCleanedData.get('sensors')):
            self._errors['sensors'] = self.error_class([
                'Please select one or more sensors.'])
            raise forms.ValidationError(
                'Error: Sensors are mandatory for sensors-based products '
                'search!')

        return self.cleaned_data


class ProductIdSearchForm(forms.ModelForm):
    """
    Form for product id search refine
    """
    k_orbit_path = NoValidationChoiceField((), required=False)
    j_frame_row = NoValidationChoiceField((), required=False)
    date_range = NoValidationChoiceField((), required=False)
    isAdvanced = forms.CharField(
        widget=forms.HiddenInput(), required=False, initial=True)

    mission = AbbreviationModelChoiceField(
        None, empty_label='All', required=False)
    sensors = AbbreviationModelChoiceField(
        None, empty_label='All', required=False)
    acquisition_mode = AbbreviationModelChoiceField(
        None, empty_label='All', required=False)
    sensor_type = AbbreviationModelChoiceField(
        None, empty_label='All', required=False)
    processing_level = AbbreviationModelChoiceField(
        None, empty_label='All', required=False)

    class Meta:
        model = Search
        fields = (
            'acquisition_mode', 'sensors', 'sensor_type', 'mission',
            'acquisition_mode', 'sensor_type', 'k_orbit_path', 'j_frame_row',
            'processing_level')

    def __init__(self, *args, **kwargs):
        """
        Populate lists and set UI CSS class
        """

        # This form cannot create new objects, only edit existing instances
        assert 'instance' in kwargs

        super(ProductIdSearchForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            try:
                self.fields[myField].widget.attrs['class'] = 'ui-corner-all'
            except AttributeError:
                pass

        search_instance = self.instance

        #self.fields['sensors'].queryset = search_instance.sensors.all()
        #if search_instance.acquisition_mode:
            #self.fields['acquisition_mode'].queryset = (
            #    AcquisitionMode.objects.filter(
            #    pk=search_instance.acquisition_mode.pk))
        #else:
            #self.fields['acquisition_mode'].queryset = (
            #    AcquisitionMode.objects.filter(
            #    sensor_type__mission_sensor__in=search_instance.sensors.all())
        #if search_instance.sensor_type:
            #self.fields['sensor_type'].queryset = (
            #    SensorType.objects.filter(pk=search_instance.sensor_type.pk))
        #else:
            #self.fields['sensor_type'].queryset = (
            #    SensorType.objects.filter(
            #    mission_sensor__in=search_instance.sensors.all())
        #if search_instance.mission:
            #self.fields['mission'].queryset = Mission.objects.filter(
            #    pk=search_instance.mission.pk)
        #else:
            #self.fields['mission'].queryset = Mission.objects.filter(
            #    missionsensor__in=search_instance.sensors.all())
        #if search_instance.processing_level:
            #self.fields['processing_level'].queryset = (
            #    search_instance.processing_level.all())
        #else:
            #self.fields['processing_level'].queryset = (
            #    ProcessingLevel.objects.all())

        self.fields['acquisition_mode'].queryset = (
            AcquisitionMode.objects.all())
        self.fields['sensor_type'].queryset = SensorType.objects.all()
        self.fields['mission'].queryset = Mission.objects.all()
        self.fields['processing_level'].queryset = (
            ProcessingLevel.objects.all())
        self.fields['sensors'].queryset = MissionSensor.objects.all()

        choices = [('', 'All')]
        choices.extend(
            [(i.local_format(), i.local_format())
                for i in search_instance.searchdaterange_set.all()])
        self.fields['date_range'].choices = choices

        row_choices = [('', 'All')]
        row_choices.extend([(l, l) for l in search_instance.getRowChoices()])
        path_choices = [('', 'All')]
        path_choices.extend([(l, l) for l in search_instance.getPathChoices()])

        self.fields['k_orbit_path'].choices = path_choices
        self.fields['j_frame_row'].choices = row_choices

    def clean_sensors(self):
        """
        Transform
        """
        data = self.cleaned_data['sensors']
        if not data:
            return MissionSensor.objects.all()
        else:
            return MissionSensor.objects.filter(pk=data.pk)

    def clean_date_range(self):
        """
        Transform
        """
        ranges = self.cleaned_data['date_range']
        if not ranges:
            return None

        try:
            start_date, end_date = SearchDateRange.from_local_format(ranges)
        except ValueError, e:
            raise forms.ValidationError('Error: date is not valid. %s' % e)
        if not start_date <= end_date:
            raise forms.ValidationError('Error: date range is not valid.')
        return {'start_date': start_date, 'end_date': end_date}

    def clean_processing_level(self):
        """
        Transform
        """
        if not self.cleaned_data['processing_level']:
            return []
        return [self.cleaned_data['processing_level']]


class AdvancedSearchFormv3(forms.ModelForm):
    """
    Let the user perform searches on sensors, by date and/or geometry
    digitised on map.
    """
    # keywords = forms.CharField(widget=forms.TextInput(
    #    attrs={'cols':'32'}),required=False)
    # Note1: the help_text strings are duplicated from the model help text
    #        since I didnt find a simple way to reuse it if adding custom
    #        fields
    # Note2: Only custom fields are added here. Fields that need no tweaking
    #        are pulled by the form generator directly from the model

    POLARISING_MODE_CHOICES = {'': 'All'}
    POLARISING_MODE_CHOICES.update(dict(RadarProduct.POLARISING_MODE_CHOICES))
    # ABP: the common part: will be searched on GenericProducts class only
    start_datepicker = forms.DateField(
        widget=DateTimeWidget(
            attrs={
                'title': 'Choose the start date for this date range.',
                'data-date_focus': 'start'}),
        required=False, label='Start date', input_formats=DATE_FORMATS,
        error_messages={
            'required': 'Entering a start date for your search is required.'},
        help_text='Start date is required. DD-MM-YYYY.')
    end_datepicker = forms.DateField(
        widget=DateTimeWidget(
            attrs={
                'title': 'Choose the end date for this date range.',
                'data-date_focus': 'end'}),
        required=False, label='End date', input_formats=DATE_FORMATS,
        error_messages={
            'required': 'Entering an end date for your search is required.'},
        help_text='End date is required. DD-MM-YYYY.')
    geometry = forms.CharField(
        widget=forms.HiddenInput(), required=False,
        help_text=(
            'Digitising an area of interest is not required but is recommended'
            '. You can use the help tab in the map area for more information '
            'on how to use the map. Draw an area of interest on the map to '
            'refine the set of search results to a specific area.'))

    geometry_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'file'}),
        required=False,
        help_text=(
            'Upload a zipped shapefile or KML/KMZ file of less than 1MB. If '
            'the shapefile contains more than one polygon, only the first will'
            ' be used. Complex polygons will increase search time.'))

    isAdvanced = forms.CharField(widget=forms.HiddenInput(), required=False)
    polarising_mode = forms.ChoiceField(
        choices=tuple(POLARISING_MODE_CHOICES.viewitems()), required=False)
    geometry = forms.CharField(
        widget=forms.HiddenInput(), required=False,
        help_text=(
            'Digitising an area of interest is not required but is recommended'
            '. You can use the help tab in the map area for more information '
            'on how to use the map. Draw an area of interest on the map to '
            'refine the set of search results to a specific area.'))
    aoi_geometry = AOIGeometryField(
        widget=forms.TextInput(attrs={'title': (
            'Enter bounding box coordinates separated by comma for Upper '
            'left and Lower right coordinates i.e. (20,-32,22,-34), or '
            'enter single coordinate which defines circle center and '
            'radius in kilometers (20,-32,100). Alternatively, digitise '
            'the clip area in the map.')
        }),
        required=False)

    k_orbit_path = IntegersCSVIntervalsField(
        required=False,
        help_text=(
            'Insert the orbit path as a list of comma separated values or '
            'ranges (e.g. : "10,20,30" or  "20-40")'))
    j_frame_row = IntegersCSVIntervalsField(
        required=False,
        help_text=(
            'Insert the frame row as a list of comma separated values or '
            'ranges (e.g. : "10,20,30" or "20-40")'))
    # exclude PRODUCT_SEARCH_GENERIC from Search.PRODUCT_SEARCH_TYPES
    search_type = forms.ChoiceField(
        choices=Search.PRODUCT_SEARCH_TYPES[1:], required=False)
    cloud_mean = forms.IntegerField(
        min_value=0, max_value=100, initial=0,
        help_text=(
            'Select the maximum cloud cover (range 0-100) when searching for '
            'images. Note that not all sensors support cloud cover filtering.')
    )

    class Meta:
        model = Search
        exclude = (
            'ip_position', 'guid', 'keywords', 'geometry_file', 'user',
            'deleted', 'processing_level')

    # add Media class for this form, rendered specific for this form
    class Media:
        js = (
            "/media/js/widget.sansa-datepicker.js",
            "/media/js/widget.sansa-daterangecontainer.js",)

    def __init__(self, *args, **kwargs):
        """
        We are using jquery tooltip to show a nice tooltip for each field. To
        ensure that each field has a title set (which is used for the tooltip
        text), this function iterates the fields of a form and sets their
        title text to the help text for that field. If the title is already
        set, its left as is.
        """

        self.helper = FormHelper()
        self.helper.form_class = 'span12 '
        self.helper.form_id = 'search_form'
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.form_action = reverse('search', kwargs={})

        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Sensors',
                    Field('sensors', template='myField.html'),
                    Field('mission', template='myField.html'),
                    Field('sensor_type', template='myField.html'),
                    Field('acquisition_mode', template='myField.html'),
                    css_id="collapseSensors",
                    css_class="in",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Product type details',
                    Field('search_type', template='myField.html'),
                    Field('license_type', template='myField.html'),
                    css_id="collapseProduct",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Image details',
                    Field('use_cloud_cover', template='myField.html'),
                    Field(
                        'sensor_inclination_angle_start',
                        template='myField.html'),
                    Field('spatial_resolution', template='myField.html'),
                    Field('cloud_mean', template='myField.html'),
                    Field(
                        'sensor_inclination_angle_end',
                        template='myField.html'),
                    Field('band_count', template='myField.html'),
                    css_id="collapseImage",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Row & path',
                    Field('k_orbit_path', template='myField.html'),
                    Field('j_frame_row', template='myField.html'),
                    css_id="collapseRP",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Geometry',
                    Field('aoi_geometry', template='myField.html'),
                    Field('geometry_file', template='myField.html'),
                    css_id="collapseGeometry",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Dates',
                    Field('start_datepicker', template='myField.html'),
                    Field('end_datepicker', template='myField.html'),
                    HTML(
                        '<a id="dr_add" title="Select the dates in the calend'
                        'ar and click here to add to the list." href="javascri'
                        'pt:void(0)"><img src="/media/images/selector-add.gif"'
                        '></a>'),
                    HTML(
                        '<a id="dr_del" title="Select the ranges in the list '
                        'and click here to remove." href="javascript:void(0)">'
                        '<img src="/media/images/selector-remove.gif"></a>'),
                    HTML(
                        '<label for="id_searchdaterange_set">Date range *</lab'
                        'el>'),
                    HTML('{{ myFormset.management_form }}'),
                    Div(
                        HTML(
                            '{% for form in myFormset.forms %}<div class="dr_r'
                            'ow"><div class="dr_input">{{ form }}</div><div cl'
                            'ass="dr_text" title="Click to select."></div></di'
                            'v>{% endfor %}'),
                        id="dr_container",
                        css_class="well well-small"
                    ),
                    css_id="collapseDates",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                css_id="accordion-search2",
                template="crispy-div-accordion.html"
            ),
            'geometry'
        )
        super(AdvancedSearchFormv3, self).__init__(*args, **kwargs)
        for myFieldName, myField in self.fields.items():
            if (not 'title' in myField.widget.attrs or
                    myField.widget.attrs['title'] == ''):
                myField.widget.attrs['title'] = myField.help_text

        self.fields['sensors'].required = True
        # Do not list empty dictionary items (avoid null searches)
        qs = AcquisitionMode.objects.order_by()
        self.fields['sensors'].queryset = (MissionSensor.objects
            .filter(pk__in=qs.distinct().values_list(
                'sensor_type__mission_sensor', flat=True))
            .filter(has_data=True)
            .order_by('name'))
        self.fields['mission'].queryset = (Mission.objects
            .filter(pk__in=qs.distinct().values_list(
                'sensor_type__mission_sensor__mission', flat=True))
            .filter(missionsensor__has_data=True))
