# Generated by Django 3.1.4 on 2024-03-21 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alone_Cook', '0007_auto_20240317_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='ingredient_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_list', models.CharField(max_length=100, verbose_name='ing_list')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='ingredient',
            field=models.CharField(max_length=100, null=True, verbose_name='ing'),
        ),
    ]