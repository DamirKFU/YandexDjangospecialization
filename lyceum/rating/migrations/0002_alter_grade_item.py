# Generated by Django 4.2.9 on 2024-03-25 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0012_alter_category_name_alter_item_name_and_more"),
        ("rating", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grade",
            name="item",
            field=models.ForeignKey(
                help_text="товар которому поставили оценку",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="grades",
                related_query_name="grades",
                to="catalog.item",
                verbose_name="пользователь",
            ),
        ),
    ]
