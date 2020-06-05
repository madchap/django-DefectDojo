# Generated by Django 2.2.12 on 2020-06-05 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0036_system_settings_email_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system_settings',
            name='slack_channel',
            field=models.CharField(blank=True, default='', help_text='Optional. Needed if you want to send global notifications.', max_length=100),
        ),
        migrations.AlterField(
            model_name='system_settings',
            name='slack_username',
            field=models.CharField(blank=True, default='', help_text='Optional. Will take your bot name otherwise.', max_length=100),
        ),
    ]
