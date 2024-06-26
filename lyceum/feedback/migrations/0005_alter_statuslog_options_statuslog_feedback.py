# Generated by Django 4.2 on 2024-03-11 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "feedback",
            "0004_alter_feedback_options_alter_feedback_mail_statuslog",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="statuslog",
            options={
                "verbose_name": "журнал состояния",
                "verbose_name_plural": "журнал состояний",
            },
        ),
        migrations.AddField(
            model_name="statuslog",
            name="feedback",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="feedback.feedback",
            ),
        ),
    ]
