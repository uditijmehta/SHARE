# Generated by Django 3.2.5 on 2022-12-22 15:42

from django.db import migrations


def move_keys_to_source_config(apps, schema_editor):
    SourceConfig = apps.get_model('share', 'SourceConfig')
    source_config_qs = (
        SourceConfig.objects.all()
        .select_related('harvester', 'transformer')
    )
    for source_config in source_config_qs:
        if source_config.harvester:
            source_config.harvester_key = source_config.harvester.key
        if source_config.transformer:
            source_config.transformer_key = source_config.transformer.key
        source_config.save()


def remove_keys_from_source_config(apps, schema_editor):
    SourceConfig = apps.get_model('share', 'SourceConfig')
    SourceConfig.objects.all().update(
        harvester_key=None,
        transformer_key=None
    )


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0064_drop_harvester_transformer_a'),
    ]

    operations = [
        migrations.RunPython(move_keys_to_source_config, remove_keys_from_source_config),
    ]