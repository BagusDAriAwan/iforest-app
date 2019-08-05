# Generated by Django 2.1.7 on 2019-08-01 04:32

from django.db import migrations, models
import django.db.models.deletion
import random_forest.models_dataset
import random_forest.models_hyperparameterRF
import random_forest.models_randomForest


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=25, unique=True)),
                ('deskripsi', models.TextField()),
                ('default_dataset', models.BooleanField(default=False)),
                ('set_label', models.BooleanField(default=False)),
                ('file_dataset', models.FileField(upload_to='dataset/csv/', validators=[random_forest.models_dataset.validate_file_extension])),
                ('separator', models.CharField(choices=[('koma', 'Koma'), ('titik_koma', 'Titik Koma'), ('tab', 'Tab'), ('enter', 'Enter')], default='koma', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='HyperparameterRF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_rf', models.BooleanField(default=False)),
                ('default_hyperparameter', models.BooleanField(default=False)),
                ('n_tree', models.IntegerField(default=10)),
                ('max_fitur', models.CharField(default='sqrt', max_length=10, validators=[random_forest.models_hyperparameterRF.validate_max_fitur])),
            ],
        ),
        migrations.CreateModel(
            name='RandomForest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k_cv', models.IntegerField(default=5, validators=[random_forest.models_randomForest.validate_k_cv])),
                ('rf_result', models.FileField(default='coba.csv', upload_to='randomForest/result/')),
                ('rf_fitur_importance', models.FileField(default='coba.csv', upload_to='randomForest/fiturImportance/')),
                ('rf_model', models.FileField(default='coba.pkl', upload_to='randomForest/model/')),
                ('tanggal_running', models.DateTimeField(auto_now_add=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='random_forest.Dataset')),
                ('hyperparameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='random_forest.HyperparameterRF')),
            ],
        ),
        migrations.CreateModel(
            name='SetFitur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jml_fitur', models.CharField(default=10, max_length=10)),
                ('fitur', models.TextField(blank=True, null=True)),
                ('default_fitur', models.BooleanField(default=False)),
                ('use_if', models.BooleanField(default=False)),
                ('all_fitur', models.BooleanField(choices=[(True, 'Ya'), (False, 'Tidak')], default=True, max_length=255)),
                ('delete_fitur_with_null_val', models.BooleanField(choices=[(True, 'Ya'), (False, 'Tidak')], default=True, max_length=255)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='random_forest.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='SetLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validate_label', models.BooleanField(default=False)),
                ('use_rf', models.BooleanField(default=False)),
                ('kolom_label', models.CharField(max_length=10)),
                ('nilai_label_kanker', models.CharField(max_length=10)),
                ('dataset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='random_forest.Dataset')),
            ],
        ),
        migrations.AddField(
            model_name='randomforest',
            name='setfitur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='random_forest.SetFitur'),
        ),
        migrations.AddField(
            model_name='randomforest',
            name='setlabel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='random_forest.SetLabel'),
        ),
    ]