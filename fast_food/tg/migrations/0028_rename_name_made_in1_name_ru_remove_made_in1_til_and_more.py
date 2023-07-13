# Generated by Django 4.0.6 on 2023-01-09 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0027_made_in1_til'),
    ]

    operations = [
        migrations.RenameField(
            model_name='made_in1',
            old_name='name',
            new_name='name_ru',
        ),
        migrations.RemoveField(
            model_name='made_in1',
            name='til',
        ),
        migrations.AddField(
            model_name='made_in1',
            name='name_uz',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
    ]