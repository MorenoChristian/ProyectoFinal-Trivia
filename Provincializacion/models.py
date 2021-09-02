from django.db import models
from django.conf import settings

from django.contrib.auth.models import User


# Necesitamos preguntas¿?, estas tienen posibles respuestas, a su vez tenemos los intentos o eleccions por el usuario
# y por ultimo tenemos al usuario, todo esto necesitamos

class Pregunta(models.Model):
    
    texto = models.TextField(verbose_name = 'Texto de la pregunta')

    def __str__(self): #Con este método le decimos a python que nos retorne el valor self.texto de la clase
        return self.texto

class ElegirRespuesta(models.Model):

    max_respuestas = 4

    #verbose_name indicamos el nombre del campo referenciado
    # con CASCADE, si eliminamos una respuesta, se eliminaran en la base de datos las dependencias que tiene con
    # las relaciones Foreingkey
    pregunta = models.ForeignKey(Pregunta, related_name='preguntas', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name="¿Es esta la respuesta correcta?" ,default=False, null=False)
    texto = models.TextField(verbose_name="Texto de la respuesta")

    def __str__(self):
        return self.texto

#Usuario que tiene una relacion uno a uno con el usuario origina, pero este almacena su nombre y el puntaje al ingresar a jugar/
class UsuarioTrivia(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name='Puntaje Total', default=0, decimal_places=2, max_digits=10)

class PreguntasRespondidas(models.Model):
    usuario = models.ForeignKey(UsuarioTrivia, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, related_name='intentos')
    correcta = models.BooleanField(verbose_name='¿Es esta la respuesta correcta?', default=False, null=False)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)
