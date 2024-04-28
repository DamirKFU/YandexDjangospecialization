# Generated by Django 4.2 on 2024-02-26 08:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_remove_category_weight"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="weight",
            field=models.IntegerField(
                default=100,
                help_text="ну какой вес то",
                validators=[
                    django.core.validators.MaxValueValidator(32767),
                    django.core.validators.MinValueValidator(1),
                ],
                verbose_name="вес",
            ),
        ),
    ]
