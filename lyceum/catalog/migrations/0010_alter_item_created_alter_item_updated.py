# Generated by Django 4.2 on 2024-03-10 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0009_item_created_item_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="дата и время создания",
                null=True,
                verbose_name="создано",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="updated",
            field=models.DateTimeField(
                editable=False,
                help_text="дата и время обновления",
                null=True,
                verbose_name="обновлено",
            ),
        ),
    ]
