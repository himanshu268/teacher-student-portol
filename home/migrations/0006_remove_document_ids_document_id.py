# Generated by Django 4.1 on 2023-06-28 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_document_ids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='ids',
        ),
        migrations.AddField(
            model_name='document',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
