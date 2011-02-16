"""
Reads DIMS tar gnu zip compressed packages and extract metadata
and/or imagery and thumbnails
"""

import os
import re
import tarfile
from datetime import datetime

try:
  from lxml import etree
except ImportError:
  import xml.etree.ElementTree as etree


class dims(object):
  """
  The main class
  """
  statuses    = ('OPEN', 'CLOSE')

  NS = dict(
    xmlns_gco   = "{http://www.isotc211.org/2005/gco}",
    xmlns_gts   = "{http://www.isotc211.org/2005/gts}",
    xmlns_gss   = "{http://www.isotc211.org/2005/gss}",
    xmlns_gsr   = "{http://www.isotc211.org/2005/gsr}",
    xmlns_xsi   = "{http://www.w3.org/2001/XMLSchema-instance}",
    xmlns_xlink = "{http://www.w3.org/1999/xlink}",
    xmlns_gml   = "{http://www.opengis.net/gml}",
    xmlns       = "{http://www.isotc211.org/2005/gmd}",
    )


  def __init__(self, path):
    """
    Set the file path
    """
    import logging
    logging.debug(self.NS)
    self._path      = path
    self._status    = None
    self._tar       = None
    self._tar_index = None
    self._products  = {}
    if os.path.isfile(path):
      self._read()

  def _read(self):
    """
    Read the tar
    """
    self._tar       = tarfile.open(self._path, 'r:gz')
    self._tar_index = self._tar.getnames()

    # Scan for DIMS products
    for product_path in filter(lambda x: re.search(self._tar_index[0] + '/' + 'Metadata/ISOMetadata/[^/]+/[^\.]+\.xml$', x), self._tar_index):
      m = re.search('ISOMetadata/([^/]+)/([^/]+)$', product_path)
      pl, pr = m.groups()
      self._products[pr] = {'path': product_path, 'metadata': self._read_metadata(product_path)}


  def _read_metadata(self, product_path):
    """
    Extract metadata from an XML metadata file object and
    returns informations as a dictionary
    """
    file_info = self._tar.getmember(product_path)
    file_handle = self._tar.extractfile(file_info)
    tree = etree.parse(file_handle)
    #TODO: missing from ISO 'spatial_coverage':     PolygonField
    metadata = {
          'product_date':             datetime.strptime(tree.find('//{xmlns}dateStamp/{xmlns_gco}Date'.format(**self.NS)).text, '%Y-%m-%dT%H:%M:%S.%f'),
          'projection' :              tree.find('//{xmlns_gml}VerticalCS/{xmlns_gml}name'.format(**self.NS)).text,
        }
    return metadata


  def get_metadata(self):
    """
    Returns metadata
    """
    return self._products

  def write(self):
    """
    Write the tarfile to disk
    """
    pass

  def __str__(self):
    """
    Print
    """
    return 'DIMS [%s]: %s ' % (self._status, self._path)


