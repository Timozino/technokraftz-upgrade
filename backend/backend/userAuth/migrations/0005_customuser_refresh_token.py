# Generated by Django 4.2.7 on 2024-06-21 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userAuth", "0004_alter_customuser_options_alter_profile_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="refresh_token",
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
