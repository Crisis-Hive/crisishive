from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Make username nullable and blank so allauth email-only signup works
    without providing a username. Existing rows are unaffected — they
    already have a username value.
    """

    dependencies = [
        ('accounts', '0002_seed_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                blank=True,
                default='',
                error_messages={'unique': 'A user with that username already exists.'},
                help_text='Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                max_length=150,
                verbose_name='username',
            ),
        ),
    ]