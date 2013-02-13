"""
SANSA-EO Catalogue - migrate catalogue to version 3.0

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '11/02/2013'
__copyright__ = 'South African National Space Agency'

import os
from optparse import make_option
import subprocess

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrate catalogue db from v2.x to v3.0, uses default database'

    option_list = BaseCommand.option_list + (
        make_option(
            '--migrations', metavar="MIGRATION_TYPE", default='all',
            help=(
                'Selectively migrate parts of the database, semicolon ";" '
                'delimited list of migrations (new_dicts, userprofiles,'
                'search) defaults to "all"')),
    )

    def handle(self, *args, **options):
        self.db = settings.DATABASES['default']['NAME']
        myMigrations = options.get('migrations').split(';')

        if 'all' in myMigrations:
            self.migrate_new_dicts()
            self.migrate_userprofiles()
            self.migrate_search()

        if 'new_dicts' in myMigrations:
            self.migrate_new_dicts()

        if 'userprofiles' in myMigrations:
            self.migrate_userprofiles()

        if 'search' in myMigrations:
            self.migrate_search()

    def migrate_new_dicts(self):
        print '* Starting new_dicts migration...'
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'sql', 'new_master'))
        print '* Executing database migration scripts...'
        subprocess.call(['sh', '001_new_dicts.sh', self.db])
        os.chdir(origWD)

    def migrate_userprofiles(self):
        print '* Starting profile migration...'
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, '..', 'sql', 'new_master'))
        print '* Executing database migration scripts...'
        subprocess.call(['sh', '002_profile_migration.sh', self.db])
        os.chdir(origWD)
        print '* Checking user permission (might take awhile)...'
        call_command('check_permissions')

    def migrate_search(self):
        print '* Starting search app migration...'
        origWD = os.getcwd()
        os.chdir(os.path.join(origWD, 'sql', 'new_master'))
        print '* Executing database migration scripts...'
        subprocess.call(['sh', '003_search_migration.sh', self.db])
        os.chdir(origWD)
