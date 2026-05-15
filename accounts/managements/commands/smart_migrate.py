"""
smart_migrate - Detects corrupted migration state and repairs it before migrating.

The problem: Railway's PostgreSQL DB sometimes has rows in django_migrations
marking migrations as "applied", but the actual tables don't exist (e.g. after
a DB reset without clearing the migrations table). Running plain `migrate` then
says "No migrations to apply" and gunicorn starts against a broken schema -> 500.

This command:
1. Checks if core tables actually exist in the DB.
2. If they don't, wipes the django_migrations table and re-runs all migrations.
3. Then runs collectstatic.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


SENTINEL_TABLES = [
    'accounts_role',
    'accounts_user',
    'feed_crisis',
]


class Command(BaseCommand):
    help = 'Check DB integrity and migrate, repairing corrupted migration state if needed.'

    def handle(self, *args, **options):
        self.stdout.write('==> smart_migrate: checking database state...')

        if self._tables_missing():
            self.stdout.write(self.style.WARNING(
                '  Core tables are missing despite migration records. '
                'Resetting django_migrations and re-running all migrations...'
            ))
            self._reset_migrations_table()
        else:
            self.stdout.write('  Tables look good. Running normal migrate...')

        call_command('migrate', '--noinput', verbosity=1)
        self.stdout.write(self.style.SUCCESS('==> smart_migrate: done.'))

    def _tables_missing(self):
        existing = connection.introspection.table_names()
        missing = [t for t in SENTINEL_TABLES if t not in existing]
        if missing:
            self.stdout.write(f'  Missing tables: {missing}')
        return bool(missing)

    def _reset_migrations_table(self):
        with connection.cursor() as cursor:
            # Check if django_migrations itself exists first
            existing = connection.introspection.table_names()
            if 'django_migrations' in existing:
                cursor.execute("DELETE FROM django_migrations;")
                self.stdout.write('  Cleared django_migrations table.')
            else:
                self.stdout.write('  django_migrations table not found — will be created by migrate.')