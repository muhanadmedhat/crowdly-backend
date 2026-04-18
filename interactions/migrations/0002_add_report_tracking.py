# Generated migration to add status and admin_notes to report models

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0001_initial'),
    ]

    operations = [
        # Add fields to ProjectReport
        migrations.AddField(
            model_name='projectreport',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('pending', 'Pending'),
                    ('reviewed', 'Reviewed'),
                    ('approved', 'Approved'),
                    ('rejected', 'Rejected'),
                ],
                default='pending',
            ),
        ),
        migrations.AddField(
            model_name='projectreport',
            name='admin_notes',
            field=models.TextField(
                blank=True,
                null=True,
                help_text='Admin notes about the report action',
            ),
        ),

        # Add fields to CommentReport
        migrations.AddField(
            model_name='commentreport',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('pending', 'Pending'),
                    ('reviewed', 'Reviewed'),
                    ('approved', 'Approved'),
                    ('rejected', 'Rejected'),
                ],
                default='pending',
            ),
        ),
        migrations.AddField(
            model_name='commentreport',
            name='admin_notes',
            field=models.TextField(
                blank=True,
                null=True,
                help_text='Admin notes about the report action',
            ),
        ),

        # Add fields to ReplyReport
        migrations.AddField(
            model_name='replyreport',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('pending', 'Pending'),
                    ('reviewed', 'Reviewed'),
                    ('approved', 'Approved'),
                    ('rejected', 'Rejected'),
                ],
                default='pending',
            ),
        ),
        migrations.AddField(
            model_name='replyreport',
            name='admin_notes',
            field=models.TextField(
                blank=True,
                null=True,
                help_text='Admin notes about the report action',
            ),
        ),
    ]
