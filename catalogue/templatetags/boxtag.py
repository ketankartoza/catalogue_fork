## Original code from Tim's SABIO project and copyright is retained by the original author #
from django import template
     
register = template.Library()     
@register.simple_tag
def box_start( heading, icon, id ):
  myString = '''
    <div class="ui-widget append-bottom">
      <div class="ui-helper-reset ui-widget-content ui-state-highlight ui-corner-all"  style="padding: 10px; min-height: 100px;" id="%s" >''' % id
  if heading:
    myString = myString + '''
    <p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>
    ''' 
    + str(heading) + '''
    </p>
    '''
  myString = myString + '''<div>'''
  return myString
    
@register.simple_tag
def box_end( ):
  return '''
        </div>
      </div>
    </div>
  '''


@register.simple_tag
def error_message_start( heading ):
  return '''
    <div class="ui-widget">
      <div class="ui-state-error ui-corner-all" style="padding: 0 .7em;"> 
        <p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>
        ''' + heading + '''
        </p>
        <div>
        '''

@register.simple_tag
def error_message_end( ):
  return '''
        </div>
      </div>
    </div>
    '''
