from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # Roles are seeded via accounts/migrations/0002_seed_roles.py.
    # The post_migrate signal approach has been removed to avoid
    # double-seeding and IntegrityErrors on a fresh Railway deployment.