from django.db import models
from django.utils import timezone

from apps.clientes.models import Cliente
from apps.servicios.models import Combo, Servicio


class Alquiler(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, default=1)
    combo = models.ForeignKey(Combo, null=True, blank=True, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, default="Sin dirección")
    fecha_hora_reserva = models.DateTimeField(default=timezone.now)
    cantidad_unidades = models.PositiveIntegerField(default=1)
    costo_total = models.FloatField()
    fecha_fin_reserva = models.DateTimeField(blank=True, null=True)
    hora_fin_planificada = models.TimeField(blank=True, null=True)
    hora_fin_real = models.TimeField(blank=True, null=True)
    calificacion_cliente = models.IntegerField(blank=True, null=True)
    calificacion_negocio = models.IntegerField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        if self.combo:
            return f"Alquiler {self.id} - Combo: {self.combo.nombre}"
        elif self.servicio:
            return f"Alquiler {self.id} - Servicio: {self.servicio.titulo}"
        return f"Alquiler {self.id} - Sin especificar"