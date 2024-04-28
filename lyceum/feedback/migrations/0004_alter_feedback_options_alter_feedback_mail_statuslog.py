# Generated by Django 4.2 on 2024-03-11 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0003_feedback_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="feedback",
            options={
                "verbose_name": "обратная связь",
                "verbose_name_plural": "обратные связи",
            },
        ),
        migrations.AlterField(
            model_name="feedback",
            name="mail",
            field=models.EmailField(
                help_text="почтовый адрес",
                max_length=254,
                verbose_name="почта",
            ),
        ),
        migrations.CreateModel(
            name="StatusLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="дата и время создания",
                        null=True,
                        verbose_name="создано",
                    ),
                ),
                (
                    "_from",
                    models.CharField(
                        choices=[
                            ("получено", "New"),
                            ("в обработке", "Pending"),
                            ("ответ дан", "Complete"),
                        ],
                        max_length=11,
                        verbose_name="от",
                    ),
                ),
                (
                    "to",
                    models.CharField(
                        choices=[
                            ("получено", "New"),
                            ("в обработке", "Pending"),
                            ("ответ дан", "Complete"),
                        ],
                        max_length=11,
                        verbose_name="от",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]