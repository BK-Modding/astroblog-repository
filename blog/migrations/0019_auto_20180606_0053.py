# Generated by Django 2.0.6 on 2018-06-06 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20180606_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='intro',
            field=models.CharField(max_length=200),
        ),
    ]
