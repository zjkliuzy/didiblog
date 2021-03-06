# Generated by Django 2.2.17 on 2021-01-29 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20210125_1529'),
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=50, verbose_name='内容')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('parent_message', models.IntegerField(default=0)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topic.Topic')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile')),
            ],
        ),
    ]
