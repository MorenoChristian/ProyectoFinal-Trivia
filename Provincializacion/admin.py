from django.contrib import admin

from .models import Pregunta, ElegirRespuesta, PreguntasRespondidas, UsuarioTrivia

class respuestaInline(admin. TabularInline):
    model = ElegirRespuesta
    can_delete = False
    max_num = ElegirRespuesta.max_respuestas

class preguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (respuestaInline, )
    list_display = ["texto", ]
    search_fields = ["texto", "preguntas__texto"]

class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['usuario','pregunta','respuesta','correcta', 'puntaje_obtenido']

admin.site.register(Pregunta, preguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(PreguntasRespondidas)
admin.site.register(UsuarioTrivia)