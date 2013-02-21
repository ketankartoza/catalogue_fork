from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Tool for harvesting data from the legacy acs catalogue
    This is a base class - you should overload it for
    each mission that you want to support.
    """

    help = "Imports LPGS Landsat records into the SANSA catalogue"
    option_list = BaseCommand.option_list + (
        make_option('--test_only', '-t', dest='test_only', action='store_true',
                    help='Just test, nothing will be written into the DB.',
                    default=False),
        make_option('--owner', '-o', dest='owner', action='store',
                    help='Name of the Institution package owner. Defaults to:'
                         ' USGS.',
                    default='USGS'),
        make_option('--creating_software', '-s', dest='creating_software',
                    action='store',
                    help='Name of the creating software. Defaults to: Unknown.',
                    default='LPGS 11.6.0'),
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

        def verblog(msg, level=1):
            if verbose >= level:
                print msg

        start_record = options.get('start_record')
        test_only = options.get('test_only')
        verbose = int(options.get('verbosity'))
        license = options.get('license')
        owner = options.get('owner')
        software = options.get('creating_software')
        quality = options.get('quality')
        halt_on_error = options.get('halt_on_error')
