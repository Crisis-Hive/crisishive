from django.db import migrations


ROLES = [
    ('Citizen',           'Can report crises, upvote, donate, and comment.'),
    ('Responder',         'First-responder; can post status updates on crises.'),
    ('Volunteer',         'Can sign up to help at a crisis site.'),
    ('Government Official', 'Can assign response teams and manage crisis status.'),
    ('Journalist',        'Can report crises and publish verified updates.'),
]


def seed_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    for name, description in ROLES:
        Role.objects.get_or_create(name=name, defaults={'description': description})


def unseed_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    Role.objects.filter(name__in=[r[0] for r in ROLES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_roles, unseed_roles),
    ]
