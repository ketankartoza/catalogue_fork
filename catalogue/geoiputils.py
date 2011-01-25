from django.shortcuts import render_to_response
from django.contrib.gis.utils.geoip import GeoIP
import re #regex support
import urllib2 

# python logging support to django logging middleware
import logging
import traceback

class GeoIpUtils:
  """A class for resolving lat/long from and IP address"""
  def __init__(self):
    """Constructor"""
    return

  def __del__(self):
    """Destructor"""
    return 

  def getMyIp(self,request):
    """
    Fetch an IP when request.META returns localhost
    """
    remote_ip = request.META['REMOTE_ADDR']
    if remote_ip == '127.0.0.1':
      checkip = urllib2.urlopen('http://checkip.dyndns.org/').read() 
      matcher = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}') 
      try:
        remote_ip = matcher.search(checkip).group()
      except:
        remote_ip = ''
    logging.info( "Remote ip is: " + remote_ip )
    return remote_ip

  def getMyLatLong(self,request):
    g = GeoIP()
    remote_ip = self.getMyIp(request)
    try:
      remote_location = g.city(remote_ip)
      if remote_location:
        logging.info( remote_location )
        return remote_location
      else: # ip cannot be found
        logging.info( "IP could not be looked up :-(" )
        return None
    except Exception, e:
      logging.info( traceback.format_exc() )
      return None

