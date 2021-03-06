# Generated by Django 2.1.4 on 2018-12-25 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Neighbor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote', models.CharField(max_length=200)),
                ('router_port', models.CharField(max_length=200)),
                ('remote_port', models.CharField(max_length=200)),
                ('router_slot', models.CharField(max_length=200)),
                ('remote_slot', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Router',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('node_type', models.CharField(max_length=200)),
                ('speed', models.CharField(max_length=200)),
                ('port_count', models.IntegerField()),
                ('state', models.CharField(max_length=200)),
                ('router', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routerApp.Router')),
            ],
        ),
        migrations.AddField(
            model_name='port',
            name='router',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routerApp.Router'),
        ),
        migrations.AddField(
            model_name='port',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routerApp.Slot'),
        ),
        migrations.AddField(
            model_name='neighbor',
            name='router',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routerApp.Router'),
        ),
        migrations.AlterUniqueTogether(
            name='slot',
            unique_together={('name', 'router')},
        ),
        migrations.AlterUniqueTogether(
            name='port',
            unique_together={('name', 'router', 'slot')},
        ),
    ]
