# Generated by Django 4.0.5 on 2022-06-09 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('creation_date', models.DateTimeField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('timestamp', models.DateTimeField()),
                ('delivered', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('destruct_timer', models.IntegerField(blank=True, default=0, null=True)),
                ('recipient', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.ManyToManyField(related_name='user_friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_friendlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
