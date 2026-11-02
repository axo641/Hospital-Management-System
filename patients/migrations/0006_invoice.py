from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_testresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'amount',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10
                    )
                ),
                (
                    'description',
                    models.TextField(blank=True)
                ),
                (
                    'issued_date',
                    models.DateField(
                        default=django.utils.timezone.localdate
                    )
                ),
                (
                    'payment_status',
                    models.CharField(
                        choices=[
                            ('UNPAID', 'Unpaid'),
                            ('PAID', 'Paid')
                        ],
                        default='UNPAID',
                        max_length=10
                    )
                ),
                (
                    'paid_at',
                    models.DateTimeField(
                        blank=True,
                        null=True
                    )
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='invoices',
                        to='patients.patient'
                    )
                ),
            ],
        ),
    ]
