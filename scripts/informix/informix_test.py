#!/usr/bin/python

import sys
import informixdb  # import the InformixDB module

# ------------------------------------
# open connection to database 'stores'
# ------------------------------------
conn = informixdb.connect('catalogue@catalog2', user='informix', password='')

# ----------------------------------
# allocate cursor and execute select
# ----------------------------------
cursor1 = conn.cursor(rowformat = informixdb.ROW_AS_DICT)
cursor1.execute('select * from t_file_types')

for row in cursor1:

    # -------------------------------------------
    # delete row if column 'code' begins with 'C'
    # -------------------------------------------
    print "%s %s" % (row['id'], row['file_type_name'])
# ---------------------------------------
# commit transaction and close connection
# ---------------------------------------
conn.close()

sys.exit(0);
