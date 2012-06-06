from catalogues.models import *
import informixdb
import sys
myConnection = informixdb.connect('catalogue@catalog2', user='informix', password='')
myCursor = myConnection.cursor(rowformat = informixdb.ROW_AS_DICT)
myCursor.execute('select first 20 * from t_medium')
for myRow in myCursor:
    myHeaderType = HeaderType.objects.get(id=int(myRow['header_type']))
    myMedium = Medium()
    myMedium.headerType = myHeaderType
    myMedium.save
Medium.objects.all()
