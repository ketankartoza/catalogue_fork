from optparse import make_option

from django.core.management.base import BaseCommand

from catalogue.ingestors import landsat


class Command(BaseCommand):
    """
    Tool for harvesting Landsat data created by LPGS.
    """

    help = 'Imports LPGS Landsat records into the SANSA catalogue'
    option_list = BaseCommand.option_list + (
        make_option('--test_only', '-t', dest='test_only', action='store_true',
                    help='Just test, nothing will be written into the DB.',
                    default=False),
        make_option('--source_dir', '-d', dest='source_dir', action='store',
                    help='Source directory containing L7 data to import.',
                    default='/mnt/cataloguestorage/imagery_processing'),
        make_option('--owner', '-o', dest='owner', action='store',
                    help='Name of the Institution package owner. Defaults to:'
                         ' USGS.',
                    default='USGS'),
        make_option('--creating_software', '-s', dest='creating_software',
                    action='store',
                    help='Name of the creating software. Defaults to: Unknown.',
                    default='LPGS'),
        make_option('--creating_software_version', '-v',
                    dest='creating_software_version',
                    action='store',
                    help='Version of creating software. Defaults to: 11.6.0.',
                    default='11.6.0'),
        make_option('--license', '-l', dest='license', action='store',
                    default='SANSA Commercial License',
                    help='Name of the license. Defaults to: SANSA Commercial '
                         'License'),
        make_option('--quality', '-q', dest='quality', action='store',
                    help='Quality code (will be created if does not exists). '
                         'Defaults to: Unknown',
                    default='Unknown'),
        make_option('--halt-on-error', '-e', dest='halt_on_error',
                    action='store',
                    help='Halt on first error that occurs and print a '
                         'stacktrace',
                    default=False),
    )

    def handle(self, *args, **options):
        """ command execution """
        test_only = options.get('test_only')
        source_dir = options.get('source_dir')
        verbose = int(options.get('verbosity'))
        software_license = options.get('license')
        owner = options.get('owner')
        software = options.get('creating_software')
        software_version = options.get('creating_software_version')
        quality = options.get('quality')
        halt_on_error = options.get('halt_on_error')
        landsat.ingest(
            theSourceDir=source_dir,
            theTestOnlyFlag=test_only,
            theVerbosityLevel=verbose,
            theLicense=software_license,
            theOwner=owner,
            theSoftware=software,
            theSoftwareVersion=software_version,
            theQuality=quality,
            theHaltOnErrorFlag=halt_on_error
        )
