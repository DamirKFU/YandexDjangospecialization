# Generated by Django 4.2.9 on 2024-03-25 18:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0012_alter_category_name_alter_item_name_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rating", "0003_alter_grade_grade_alter_grade_item"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="grade",
            unique_together={("user", "item")},
        ),
    ]
