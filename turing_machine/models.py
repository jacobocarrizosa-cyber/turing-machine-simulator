# -*- coding: utf-8 -*-
from django.db import models

class TuringMachine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    mt_file = models.FileField(upload_to='turing_files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Execution(models.Model):
    STATUS_CHOICES = [
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
        ('No Termina', 'No Termina (Límite de pasos superado)'),
    ]

    turing_machine = models.ForeignKey(TuringMachine, on_delete=models.CASCADE, related_name='executions')
    input_string = models.CharField(max_length=255, blank=True)
    final_tape = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    steps_count = models.IntegerField(default=0)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.turing_machine.name} - {self.input_string or 'λ'} ({self.status})"