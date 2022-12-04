# Generated by Django 4.1.3 on 2022-12-03 02:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0004_alter_profile_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hashtag",
            fields=[
                ("title", models.CharField(max_length=200)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("title", models.CharField(blank=True, max_length=300, null=True)),
                ("content", models.TextField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("hashtags", models.ManyToManyField(blank=True, to="post.hashtag")),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.profile"
                    ),
                ),
            ],
        ),
    ]