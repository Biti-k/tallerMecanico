# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser


class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nif = models.CharField(db_column='NIF', primary_key=True, max_length=9)  # Field name made lowercase.
    email = models.CharField(max_length=255, blank=True, null=True)
    telf = models.CharField(max_length=9, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre + " " + self.apellido + " - " + self.nif
    
    class Meta:
        managed = False
        db_table = 'cliente'


class Coche(models.Model):
    matricula = models.CharField(primary_key=True, max_length=7)
    modelo = models.ForeignKey('MarcaModelo', models.DO_NOTHING, db_column='modelo')
    km = models.IntegerField(db_column='kM')  # Field name made lowercase.
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente')

    def __str__(self):
        return self.matricula + " - " + self.modelo.modelo
    
    class Meta:
        managed = False
        db_table = 'coche'


class Contador(models.Model):
    concepto = models.CharField(max_length=50)
    comptador = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'contador'


class Factura(models.Model):
    fecha = models.DateField()
    reparacion = models.ForeignKey('Reparacion', models.DO_NOTHING, db_column='reparacion')
    n_factura = models.CharField(primary_key=True, max_length=255)
    base = models.FloatField()
    t_iva = models.FloatField(db_column='t_IVA')  # Field name made lowercase.
    precio_obra = models.FloatField()
    precio_total = models.FloatField()
    pagado = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'factura'


class Linea(models.Model):
    tarea = models.CharField(max_length=255)
    reparacion = models.ForeignKey('Reparacion', models.DO_NOTHING, db_column='reparacion')
    pack = models.ForeignKey('Pack', models.DO_NOTHING, db_column='pack', blank=True, null=True)
    cantidad = models.FloatField()
    precio = models.FloatField(blank=True, null=True)
    precio_total = models.FloatField(blank=True, null=True)
    tipo = models.ForeignKey('TipoLinea', models.DO_NOTHING, db_column='tipo')
    descuento = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linea'


class MarcaModelo(models.Model):
    modelo = models.CharField(max_length=255)
    clasificacion_energetica = models.FloatField(db_column='Clasificacion_Energetica', blank=True, null=True)  # Field name made lowercase.
    consumo_minimo = models.FloatField(db_column='Consumo_Minimo', blank=True, null=True)  # Field name made lowercase.
    consumo_maximo = models.FloatField(db_column='Consumo_Maximo', blank=True, null=True)  # Field name made lowercase.
    emisiones_minimo = models.FloatField(db_column='Emisiones_Minimo', blank=True, null=True)  # Field name made lowercase.
    emisiones_maximo = models.FloatField(db_column='Emisiones_Maximo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'marca_modelo'


class Pack(models.Model):
    accion = models.CharField(max_length=255)
    coste = models.FloatField()

    class Meta:
        managed = False
        db_table = 'pack'


class Reparacion(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='Cliente')  # Field name made lowercase.
    coche = models.ForeignKey(Coche, models.DO_NOTHING, db_column='Coche')  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=1)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reparacion'


class TipoLinea(models.Model):
    tipo = models.CharField(primary_key=True, max_length=1)
    desc = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tipo_linea'


class Usuario(models.Model):
    login_nombre = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50)
    nif = models.CharField(db_column='NIF', primary_key=True, max_length=9)  # Field name made lowercase.
    password = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'usuario'
