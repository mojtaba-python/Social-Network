# Generated by Django 5.0 on 2024-02-17 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='titr',
            field=models.CharField(default=False, max_length=10),
        ),
    ]
