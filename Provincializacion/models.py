from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
import random

from django.db.models.fields import related


# Necesitamos preguntas¿?, estas tienen posibles respuestas, a su vez tenemos los intentos o eleccions por el usuario
# y por ultimo tenemos al usuario, todo esto necesitamos

class Pregunta(models.Model):
    
    texto = models.TextField(verbose_name = 'Texto de la pregunta')
    max_puntaje = models.DecimalField(verbose_name='Maximo Puntaje', default=3, decimal_places=2, max_digits=6)

    def __str__(self): #Con este método le decimos a python que nos retorne el valor self.texto de la clase
        return self.texto

class ElegirRespuesta(models.Model):

    max_respuestas = 4

    #verbose_name indicamos el nombre del campo referenciado
    # con CASCADE, si eliminamos una respuesta, se eliminaran en la base de datos las dependencias que tiene con
    # las relaciones Foreingkey
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name="¿Es esta la respuesta correcta?" ,default=False, null=False)
    texto = models.TextField(verbose_name="Texto de la respuesta")

    def __str__(self):
        return self.texto

#Usuario que tiene una relacion uno a uno con el usuario origina, pero este almacena su nombre y el puntaje al ingresar a jugar/
class UsuarioTrivia(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name='Puntaje Total', default=0, decimal_places=2, max_digits=10)

    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, usuariotrivia=self)
        intento.save()

    def obtener_nuevas_preguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(usuariotrivia=self).values_list('pregunta__pk', flat=True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)
    
    def validar_intento(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return
        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada
        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_seleccionada
        
        else:
            pregunta_respondida.respuesta = respuesta_seleccionada

        
        pregunta_respondida.save()

        self.actualizar_puntaje()




    def actualizar_puntaje(self):
        puntaje_actualizado= self.intentos.filter(correcta=True).aggregate(
            models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']
        
        self.puntaje_total = puntaje_actualizado
        self.save()  
        

class PreguntasRespondidas(models.Model):
    usuariotrivia = models.ForeignKey(UsuarioTrivia, on_delete=models.CASCADE, related_name='intentos')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField(verbose_name='¿Es esta la respuesta correcta?', default=False, null=False)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)
