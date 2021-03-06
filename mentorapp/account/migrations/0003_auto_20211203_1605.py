# Generated by Django 2.1.5 on 2021-12-03 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20211203_1140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterField(
            model_name='mentee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.User'),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.User'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='msg_content',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='msg',
            name='receipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipient', to='account.User'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='account.User'),
        ),
    ]
