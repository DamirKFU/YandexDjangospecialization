# Generated by Django 4.2 on 2024-03-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_alter_category_normalize_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="создано"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="updated",
            field=models.DateTimeField(
                editable=False, null=True, verbose_name="обновлено"
            ),
        ),
    ]