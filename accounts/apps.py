from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(load_roles, sender=self)


def load_roles(sender, **kwargs):
    from accounts.models import Role
    if Role.objects.exists():
        return  # already loaded, skip
    roles = [
        {'name': 'Citizen', 'description': 'General public who can report crises and volunteer.'},
        {'name': 'Volunteer', 'description': 'Community volunteer who responds to crises on the ground.'},
        {'name': 'Relief Team', 'description': 'Organized relief/rescue team that responds to crises.'},
        {'name': 'Responder', 'description': 'Official response team member (fire, medical, rescue etc.).'},
        {'name': 'Government', 'description': 'Government official who monitors and oversees crisis resolution.'},
        {'name': 'Journalist', 'description': 'Media personnel who follows and reports on crises.'},
        {'name': 'Admin', 'description': 'Platform administrator with full access.'},
    ]
    roles = [
        {'name': 'Citizen',   'description': 'General public who can report crises and volunteer.'},
        {'name': 'Volunteer', 'description': 'Community volunteer who responds to crises on the ground.'},
        {'name': 'Responder', 'description': 'Official response team member (fire, medical, rescue etc.).'},
        {'name': 'Admin',     'description': 'Platform administrator with full access.'},
    ]
    for r in roles:
        Role.objects.create(**r)
    print(f"[CrisisHive] Loaded {len(roles)} roles.")
