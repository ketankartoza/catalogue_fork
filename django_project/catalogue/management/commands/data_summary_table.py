__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '4/27/16'

from django.db.models.query import QuerySet
from django.contrib.gis.db import models
from catalogue.dbhelpers import executeRAWSQL
from django.db.models import Count
from dictionaries.models import SatelliteInstrumentGroup
from django.core.management.base import BaseCommand


halt_on_error = True
# dir_path=('/home/web/django_project/media/')

class Command(BaseCommand):
    args = 'path'
    help = 'Store data range data summary table from raw query'

    def get_instrument_group_id(self):
        instrument_group_id = executeRAWSQL("""
            SELECT satellite_instrument_group_id
            from dictionaries_satelliteinstrument;""")

        inst_list = []
        for i in range(len(instrument_group_id)):
            inst_list.append(instrument_group_id[i]['satellite_instrument_group_id'])

        return inst_list

    def get_satellite_instrument_type(self, instrument_id=1):
        data = executeRAWSQL("""
            select dictionaries_satellite.operator_abbreviation as satellite,
            dictionaries_instrumenttype.operator_abbreviation as instrument_type
            from dictionaries_satellite, dictionaries_instrumenttype,
            dictionaries_satelliteinstrumentgroup
            where dictionaries_satellite.id=dictionaries_satelliteinstrumentgroup.satellite_id
            AND dictionaries_instrumenttype.id=dictionaries_satelliteinstrumentgroup.instrument_type_id
            and dictionaries_satelliteinstrumentgroup.id=
            %(instrument_id)s;""", {'instrument_id': instrument_id})

        return data

    def get_product_per_year(self, inst_id):
        myStats = executeRAWSQL("""
            SELECT count(*) as count, extract(YEAR from gp.product_date)::int as year
            FROM
              catalogue_genericproduct gp, catalogue_genericimageryproduct gip,
              catalogue_genericsensorproduct gsp, catalogue_opticalproduct op,
              dictionaries_opticalproductprofile opp, dictionaries_satelliteinstrument si
            WHERE
              gip.genericproduct_ptr_id = gp.id AND
              gsp.genericimageryproduct_ptr_id = gip.genericproduct_ptr_id AND
              op.genericsensorproduct_ptr_id = gsp.genericimageryproduct_ptr_id AND
              opp.id = op.product_profile_id AND opp.satellite_instrument_id = si.id
            AND si.satellite_instrument_group_id=%(sensor_pk)s
            GROUP BY extract(YEAR from gp.product_date)
            ORDER BY year ASC;""", {'sensor_pk': inst_id})
        return myStats

    def handle(self, *args, **options):
        """Implementation for command

        :param args: path for the result files '/home/web/django_project/media/'
        :type args: str

        :raises: IOError

        """

        if len(args) < 1:
            self.stdout.write("Need argument for result path "
                              "ex : /home/web/django_project/media/")
            return

        path = args[0]
        inst_list = list(set(self.get_instrument_group_id()))

        for inst_id in inst_list:
            file_name = "output.txt"
            text_file = open(path + file_name, "a")
            text_file.write("satellite: {}, instrument_type: {}\n".format(
                self.get_satellite_instrument_type(inst_id)[0]['satellite'],
                self.get_satellite_instrument_type(inst_id)[0]['instrument_type']))
            print "write satellite and instrument type.."
            try:
                print "write min year..."
                min_year = self.get_product_per_year(inst_id)[1]['year']
                text_file.write("start_year : {}\n".format(min_year))
            except:
                text_file.write("start_year : - \n")
            try:
                print "write max year"
                max_year = self.get_product_per_year(inst_id)[-1]['year']
                text_file.write("end_year : {}\n".format(max_year))
            except:
                text_file.write("end_year : - \n")
            continue
            text_file.close()
