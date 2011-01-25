# -*- coding: utf-8 -*-
from django.utils.encoding import force_unicode
from django.conf import settings
from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
import logging

class GeometryWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    """name - the name for the widget
    value - the value for the widget (e.g. when using the form to edit)
    attrs - the widget attributes as specified in the attrs={}
    area in the form class
    """
    logging.info( "GeometryWidget started" )
    # Make sure the field value is always valid
    if value is None: value = ''
    # Get any attributes the form designer may have specified
    attrs = self.build_attrs(attrs, type=self.input_type, name=name)
    # Always ensure there is an id attribute for the field
    attrs['type'] = 'hidden'
    if not attrs.has_key('id'):
      attrs['id'] = 'id_%s' % (name)
      # Lets customise the css a little now - with a big bold font
      # We append any user specified attributes to our custom ones
    if attrs.has_key('style'):
      attrs['style'] = "font-weight: bold; font-size: 30px; height: 50px; " + attrs['style']
    else:
      attrs['style'] = ""
      # Now we write our widget into a string
    myResult = '<input %s value="%s"><div id="map"></div>' % (forms.util.flatatt(attrs), value)
    # Mark the widget html as safe - e.g. by escaping any special chars etc
    # and then return it
    return mark_safe(myResult)

