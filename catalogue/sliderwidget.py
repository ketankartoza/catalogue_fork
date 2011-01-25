from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe

# Our custom widget inherits from TextInput
class SliderWidget(forms.TextInput):
  # we simply overload the render method with our own version
  def render(self, name, value, attrs=None):
    """name - the name for the widget
       value - the value for the widget (e.g. when using the form to edit)
       attrs - the widget attributes as specified in the attrs={}
               area in the form class
    """
    # Make sure the field value is always valid
    if value is None: value = ''
    # Get any attributes the form designer may have specified
    attrs = self.build_attrs(attrs, type=self.input_type, name=name)
    # Always ensure there is an id attribute for the field
    if not attrs.has_key('id'):
      attrs['id'] = '%s_id' % (name)
    # Now we write our widget into a string
    myId = attrs['id']
    myName = attrs['name']
    myResult = """<div class="slider-panel" id="%sSliderPanel">
                    <div  class="slider-reduce-label" id="%sReduceLabel"></div>
                    <div id="%sSliderHandle"></div>
                    <div id="%sSlider"></div>
                    <div class="slider-bubble" id="%sSliderBubble"></div>
                  </div>
                  <div class="slider-increase-label" id="%sIncreaseLabel"></div>
                  <input name="%s" type="hidden" id="%s" value="%s"></input>""" % ( myId, myId, myId, myId, myId, myId, myName, myId, value )

    # Mark the widget html as safe - e.g. by escaping any special chars etc
    # and then return it
    return mark_safe(myResult)

