# Generated by Django 4.2.9 on 2024-03-22 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_profile_deactivation_date_profile_login_attempts"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="login_attempts",
            new_name="attempts_count",
        ),
    ]
