# Generated by Django 3.2.1 on 2021-06-16 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=255)),
                ('city', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Persones',
            },
        ),
        migrations.CreateModel(
            name='Racine',
            fields=[
                ('id_rac', models.BigAutoField(primary_key=True, serialize=False)),
                ('rac', models.CharField(max_length=30)),
                ('type_rac', models.IntegerField()),
                ('classe_rac', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id_sch', models.BigAutoField(primary_key=True, serialize=False)),
                ('sch_cons', models.CharField(max_length=30)),
                ('sch_voy', models.CharField(max_length=30)),
                ('scheme', models.CharField(max_length=50, null=True)),
                ('type_scheme', models.IntegerField()),
                ('classe_sch', models.CharField(max_length=100)),
                ('nombre', models.CharField(choices=[('مفرد', 'مفرد'), ('مثنى', 'مثنى'), ('جمع', 'جمع')], max_length=100)),
                ('unit', models.CharField(choices=[('مذكر', 'مفرد'), ('مؤنث', 'مثنى'), ('مذكر\\مؤنث', 'مذكر\\مؤنث')], max_length=100)),
                ('ora', models.CharField(choices=[('متكلم', 'متكلم'), ('مخاطب', 'مخاطب'), ('غائب', 'غائب')], max_length=100)),
                ('conj', models.CharField(choices=[('ماضي', 'ماضي'), ('حاظر', 'حاظر'), ('أمر', 'أمر')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Verbe',
            fields=[
                ('id_ver', models.BigAutoField(primary_key=True, serialize=False)),
                ('verbe', models.CharField(max_length=80, null=True)),
                ('ver_cons', models.CharField(max_length=30)),
                ('ver_voy', models.CharField(max_length=30)),
                ('racine_ver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.racine')),
                ('scheme_ver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.scheme')),
            ],
        ),
        migrations.CreateModel(
            name='Nom',
            fields=[
                ('id_nom', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=80, null=True)),
                ('nom_cons', models.CharField(max_length=30)),
                ('nom_voy', models.CharField(max_length=30)),
                ('racine_nom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.racine')),
                ('scheme_nom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.scheme')),
            ],
        ),
    ]
