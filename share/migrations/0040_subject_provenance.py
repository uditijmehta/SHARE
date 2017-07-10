# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 21:10
from __future__ import unicode_literals

from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models

import db.deletion


def improvenance_subjects(apps, schema_editor):
    Subject = apps.get_model('share', 'Subject')
    SubjectTaxonomy = apps.get_model('share', 'SubjectTaxonomy')
    ShareUser = apps.get_model('share', 'ShareUser')
    NormalizedData = apps.get_model('share', 'NormalizedData')

    user = ShareUser.objects.get(username=settings.APPLICATION_USERNAME)
    central_taxonomy = SubjectTaxonomy.objects.get_or_create(source=user.source)

    if not Subject.objects.exists():
        return

    normalized_data = NormalizedData.objects.create(
        source=user,
        data={
            '@graph': [
                {
                    '@id': '_:{}'.format(s.id),
                    '@type': 'subject',
                    'name': s.name,
                    'parent': None if s.parent_id is None else {'@id': '_:{}'.format(s.parent_id), '@type': 'subject'}
                } for s in Subject.objects.all()
            ]
        }
    )
    from share.tasks import disambiguate
    disambiguate.apply((normalized_data.id,), throw=True)


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0039_subject_taxonomy_a'),
    ]

    operations = [
        migrations.RunPython(improvenance_subjects),
    ]