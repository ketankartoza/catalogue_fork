"""
Unit tests for DIMS
"""


__test__ = {"doctest": """

>>> import os
>>> from catalogue.dims_lib import dims
>>> d = dims(os.path.join(os.path.split(__file__)[0], 'dims_packages', 'ORD_420882_20110124_20110124_SPOT-_V01_1.tar.gz'))
>>> d.get_metadata() # doctest:+ELLIPSIS
{'S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT-.xml': {'path': 'ORD_420882_20110124_20110124_SPOT-_V01_1/Metadata/ISOMetadata/DN_L1A/S5-_HRG_B--_CAM2_0094_00_0367_00_110122_092557_L1A-_ORBIT-.xml', 'thumbnail': <tarfile.ExFileObject object at ...>, 'metadata': {'product_date': '2011-01-24T14:29:43.278', 'cloud_cover_percentage': None, 'projection': 'ORBIT', 'processing_level_code': 'L1A'}}}


"""}