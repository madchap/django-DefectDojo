# Generated by Django 2.2.17 on 2020-12-22 13:07

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0067_max_dupes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='risk_acceptance',
            old_name='compensating_control',
            new_name='decision_details',
        ),
        migrations.AddField(
            model_name='finding',
            name='sla_start_date',
            field=models.DateField(blank=True, help_text="The date used as start date for SLA calculation. Set by expiring risk acceptances. Empty by default, causing a fallback to 'date'.", null=True, verbose_name='SLA Start Date'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='risk_acceptance_expiry',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('slack', 'slack'), ('msteams', 'msteams'), ('mail', 'mail'), ('alert', 'alert')], default='alert', help_text='Get notified of (upcoming) Risk Acceptance expiries', max_length=24, verbose_name='Risk Acceptance Expiryh'),
        ),
        migrations.AddField(
            model_name='risk_acceptance',
            name='recommendation_details',
            field=models.TextField(blank=True, help_text='Explanation of recommendation', null=True),
        ),
        migrations.AddField(
            model_name='risk_acceptance',
            name='restart_sla_expired',
            field=models.BooleanField(default=False, help_text='When enabled, the SLA for findings is restarted when the risk acceptance expires', verbose_name='Restart SLA on expiration'),
        ),
        migrations.AddField(
            model_name='system_settings',
            name='risk_acceptance_form_default_days',
            field=models.IntegerField(blank=True, default=180, help_text='Default expiry period for risk acceptance form.', null=True),
        ),
        migrations.AddField(
            model_name='system_settings',
            name='risk_acceptance_notify_expired',
            field=models.IntegerField(blank=True, default=10, help_text='Notify X days before risk acceptance expires. Leave empty to disable.', null=True),
        ),
        migrations.AlterField(
            model_name='child_rule',
            name='match_field',
            field=models.CharField(choices=[('id', 'id'), ('title', 'title'), ('date', 'date'), ('sla_start_date', 'sla_start_date'), ('cwe', 'cwe'), ('cve', 'cve'), ('cvssv3', 'cvssv3'), ('url', 'url'), ('severity', 'severity'), ('description', 'description'), ('mitigation', 'mitigation'), ('impact', 'impact'), ('steps_to_reproduce', 'steps_to_reproduce'), ('severity_justification', 'severity_justification'), ('references', 'references'), ('test', 'test'), ('is_template', 'is_template'), ('active', 'active'), ('verified', 'verified'), ('false_p', 'false_p'), ('duplicate', 'duplicate'), ('duplicate_finding', 'duplicate_finding'), ('out_of_scope', 'out_of_scope'), ('under_review', 'under_review'), ('review_requested_by', 'review_requested_by'), ('under_defect_review', 'under_defect_review'), ('defect_review_requested_by', 'defect_review_requested_by'), ('is_Mitigated', 'is_Mitigated'), ('thread_id', 'thread_id'), ('mitigated', 'mitigated'), ('mitigated_by', 'mitigated_by'), ('reporter', 'reporter'), ('numerical_severity', 'numerical_severity'), ('last_reviewed', 'last_reviewed'), ('last_reviewed_by', 'last_reviewed_by'), ('line_number', 'line_number'), ('sourcefilepath', 'sourcefilepath'), ('sourcefile', 'sourcefile'), ('param', 'param'), ('payload', 'payload'), ('hash_code', 'hash_code'), ('line', 'line'), ('file_path', 'file_path'), ('component_name', 'component_name'), ('component_version', 'component_version'), ('static_finding', 'static_finding'), ('dynamic_finding', 'dynamic_finding'), ('created', 'created'), ('scanner_confidence', 'scanner_confidence'), ('sonarqube_issue', 'sonarqube_issue'), ('unique_id_from_tool', 'unique_id_from_tool'), ('vuln_id_from_tool', 'vuln_id_from_tool'), ('sast_source_object', 'sast_source_object'), ('sast_sink_object', 'sast_sink_object'), ('sast_source_line', 'sast_source_line'), ('sast_source_file_path', 'sast_source_file_path'), ('nb_occurences', 'nb_occurences')], max_length=200),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='sla_breach',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('slack', 'slack'), ('msteams', 'msteams'), ('mail', 'mail'), ('alert', 'alert')], default='alert', help_text='Get notified of (upcoming) SLA breaches', max_length=24, verbose_name='SLA breach'),
        ),
        migrations.AlterField(
            model_name='risk_acceptance',
            name='accepted_by',
            field=models.CharField(blank=True, default=None, help_text='The entity or person that accepts the risk, can be outside of defect dojo.', max_length=200, null=True, verbose_name='Accepted By'),
        ),
        migrations.AlterField(
            model_name='risk_acceptance',
            name='expiration_date',
            field=models.DateTimeField(blank=True, default=None, help_text='When the risk acceptance expires, the findings will be reactivated', null=True),
        ),
        migrations.AlterField(
            model_name='risk_acceptance',
            name='owner',
            field=models.ForeignKey(help_text='User in defect dojo owning this acceptance. Only the owner and staff users can edit the risk acceptance.', on_delete=django.db.models.deletion.CASCADE, to='dojo.Dojo_User'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='applied_field',
            field=models.CharField(choices=[('id', 'id'), ('title', 'title'), ('date', 'date'), ('sla_start_date', 'sla_start_date'), ('cwe', 'cwe'), ('cve', 'cve'), ('cvssv3', 'cvssv3'), ('url', 'url'), ('severity', 'severity'), ('description', 'description'), ('mitigation', 'mitigation'), ('impact', 'impact'), ('steps_to_reproduce', 'steps_to_reproduce'), ('severity_justification', 'severity_justification'), ('references', 'references'), ('test', 'test'), ('is_template', 'is_template'), ('active', 'active'), ('verified', 'verified'), ('false_p', 'false_p'), ('duplicate', 'duplicate'), ('duplicate_finding', 'duplicate_finding'), ('out_of_scope', 'out_of_scope'), ('under_review', 'under_review'), ('review_requested_by', 'review_requested_by'), ('under_defect_review', 'under_defect_review'), ('defect_review_requested_by', 'defect_review_requested_by'), ('is_Mitigated', 'is_Mitigated'), ('thread_id', 'thread_id'), ('mitigated', 'mitigated'), ('mitigated_by', 'mitigated_by'), ('reporter', 'reporter'), ('numerical_severity', 'numerical_severity'), ('last_reviewed', 'last_reviewed'), ('last_reviewed_by', 'last_reviewed_by'), ('line_number', 'line_number'), ('sourcefilepath', 'sourcefilepath'), ('sourcefile', 'sourcefile'), ('param', 'param'), ('payload', 'payload'), ('hash_code', 'hash_code'), ('line', 'line'), ('file_path', 'file_path'), ('component_name', 'component_name'), ('component_version', 'component_version'), ('static_finding', 'static_finding'), ('dynamic_finding', 'dynamic_finding'), ('created', 'created'), ('scanner_confidence', 'scanner_confidence'), ('sonarqube_issue', 'sonarqube_issue'), ('unique_id_from_tool', 'unique_id_from_tool'), ('vuln_id_from_tool', 'vuln_id_from_tool'), ('sast_source_object', 'sast_source_object'), ('sast_sink_object', 'sast_sink_object'), ('sast_source_line', 'sast_source_line'), ('sast_source_file_path', 'sast_source_file_path'), ('nb_occurences', 'nb_occurences')], max_length=200),
        ),
        migrations.AlterField(
            model_name='rule',
            name='match_field',
            field=models.CharField(choices=[('id', 'id'), ('title', 'title'), ('date', 'date'), ('sla_start_date', 'sla_start_date'), ('cwe', 'cwe'), ('cve', 'cve'), ('cvssv3', 'cvssv3'), ('url', 'url'), ('severity', 'severity'), ('description', 'description'), ('mitigation', 'mitigation'), ('impact', 'impact'), ('steps_to_reproduce', 'steps_to_reproduce'), ('severity_justification', 'severity_justification'), ('references', 'references'), ('test', 'test'), ('is_template', 'is_template'), ('active', 'active'), ('verified', 'verified'), ('false_p', 'false_p'), ('duplicate', 'duplicate'), ('duplicate_finding', 'duplicate_finding'), ('out_of_scope', 'out_of_scope'), ('under_review', 'under_review'), ('review_requested_by', 'review_requested_by'), ('under_defect_review', 'under_defect_review'), ('defect_review_requested_by', 'defect_review_requested_by'), ('is_Mitigated', 'is_Mitigated'), ('thread_id', 'thread_id'), ('mitigated', 'mitigated'), ('mitigated_by', 'mitigated_by'), ('reporter', 'reporter'), ('numerical_severity', 'numerical_severity'), ('last_reviewed', 'last_reviewed'), ('last_reviewed_by', 'last_reviewed_by'), ('line_number', 'line_number'), ('sourcefilepath', 'sourcefilepath'), ('sourcefile', 'sourcefile'), ('param', 'param'), ('payload', 'payload'), ('hash_code', 'hash_code'), ('line', 'line'), ('file_path', 'file_path'), ('component_name', 'component_name'), ('component_version', 'component_version'), ('static_finding', 'static_finding'), ('dynamic_finding', 'dynamic_finding'), ('created', 'created'), ('scanner_confidence', 'scanner_confidence'), ('sonarqube_issue', 'sonarqube_issue'), ('unique_id_from_tool', 'unique_id_from_tool'), ('vuln_id_from_tool', 'vuln_id_from_tool'), ('sast_source_object', 'sast_source_object'), ('sast_sink_object', 'sast_sink_object'), ('sast_source_line', 'sast_source_line'), ('sast_source_file_path', 'sast_source_file_path'), ('nb_occurences', 'nb_occurences')], max_length=200),
        ),
        migrations.AddField(
            model_name='risk_acceptance',
            name='decision',
            field=models.CharField(choices=[('A', 'Accept'), ('V', 'Avoid'), ('C', 'Compensate'), ('R', 'Reduce'), ('T', 'Transfer')], default='A', help_text='Risk treatment decision by risk owner', max_length=2),
        ),
        migrations.AlterField(
            model_name='risk_acceptance',
            name='path',
            field=models.FileField(blank=True, null=True, upload_to='risk/%Y/%m/%d', verbose_name='Proof'),
        ),
        migrations.AddField(
            model_name='risk_acceptance',
            name='recommendation',
            field=models.CharField(choices=[('A', 'Accept'), ('V', 'Avoid'), ('C', 'Compensate'), ('R', 'Reduce'), ('T', 'Transfer')], default='R', help_text='Recommendation from the security team.', max_length=2),
        ),
        migrations.AddField(
            model_name='risk_acceptance',
            name='reactivate_expired',
            field=models.BooleanField(default=True, help_text='Reactivate findings when risk acceptance expires?', verbose_name='Reactivate findings on expiration'),
        ),
        migrations.AddField(
            model_name='product',
            name='enable_full_risk_acceptance',
            field=models.BooleanField(default=True, help_text='Allows full risk acceptanc using a risk acceptance form, expiration date, uploaded proof, etc.'),
        ),
        # convert existing products to have simple risk acceptance enabled as before
        migrations.AddField(
            model_name='product',
            name='enable_simple_risk_acceptance',
            field=models.BooleanField(default=True, help_text='Allows simple risk acceptance by checking/unchecking a checkbox.'),
        ),
        # new products will have simple risk acceptance disabled
        migrations.AlterField(
            model_name='product',
            name='enable_simple_risk_acceptance',
            field=models.BooleanField(default=False, help_text='Allows simple risk acceptance by checking/unchecking a checkbox.'),
        ),
    ]
