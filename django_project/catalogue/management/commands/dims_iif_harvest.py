"""
SANSA-EO Catalogue - DIMS IIF metadata importer - management command.

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without express permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""
from optparse import make_option
from django.core.management.base import BaseCommand
from catalogue.ingestors import dims_iif


class Command(BaseCommand):
    """
    Tool for harvesting DIMS IIF xml file for Landsat data created by DIMS.
    """

    # noinspection PyShadowingBuiltins
    help = 'Imports DIMS Landsat records into the SANSA catalogue'
    option_list = BaseCommand.option_list + (
        make_option('--test_only', '-t', dest='test_only', action='store_true',
                    help='Just test, nothing will be written into the DB.',
                    default=False),
        make_option('--source_dir', '-d', dest='source_dir', action='store',
                    help=(
                        'Source directory containing DIMS IIF xml file and '
                        'thumbnail to import.'),
                    default=(
                        '/home/web/catalogue/django_project/catalogue'
                        '/tests/sample_files/landsat/')),
        make_option('--halt_on_error', '-e', dest='halt_on_error',
                    action='store',
                    help=(
                        'Halt on first error that occurs and print a '
                        'stacktrace'),
                    default=False)
    )

    def handle(self, *args, **options):
        """ command execution """
        test_only = options.get('test_only')
        source_dir = options.get('source_dir')
        verbose = int(options.get('verbosity'))
        halt_on_error = options.get('halt_on_error')
        dims_iif.ingest(
            source_path=source_dir,
            test_only_flag=test_only,
            verbosity_level=verbose,
            halt_on_error_flag=halt_on_error
        )
