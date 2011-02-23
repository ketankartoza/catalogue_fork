# Miscellaneous views, mostly static
from catalogue.renderDecorator import renderWithContext
from helpers import *

#renderWithContext is explained in renderWith.py
@renderWithContext('index.html')
def index(theRequest):
  #render_to_response is done by the renderWithContext decorator
  myProfile = None
  return ( {
        'myPartnerFlag' : isStrategicPartner(theRequest)
      }
    )

#renderWithContext is explained in renderWith.py
@renderWithContext('about.html')
def about(theRequest):
  #render_to_response is done by the renderWithContext decorator
  return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('contact.html')
def contact(theRequest):
  #render_to_response is done by the renderWithContext decorator
  return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('mapHelp.html')
def mapHelp(theRequest):
  #render_to_response is done by the renderWithContext decorator
  if theRequest.is_ajax():
    return ( {"myTemplate" : "emptytemplate.html"})
  else:
    return ( {"myTemplate" : "base.html"})

#renderWithContext is explained in renderWith.py
@renderWithContext('emptyCartHelp.html')
def emptyCartHelp(theRequest):
  #render_to_response is done by the renderWithContext decorator
  return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('positionNotFound.html')
def positionNotFound(theRequest):
  #render_to_response is done by the renderWithContext decorator
  return ()

#Note: Dont use the login required decorator here -
# it causes the page to continually try to reload and cpu
# for firefix goes ballistic
#renderWithContext is explained in renderWith.py
@renderWithContext('sceneIdHelp.html')
def sceneIdHelp(theRequest):
  return
