# Generated by Django 5.0 on 2024-05-23 15:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("modeler", "0003_message_chat"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="title",
            field=models.CharField(
                default="Untitled diagram",
                max_length=64,
                verbose_name="name of the diagram",
            ),
        ),
    ]