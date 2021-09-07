from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from Provincializacion.models import UsuarioTrivia, Pregunta, PreguntasRespondidas
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UserRegisterForm, UsuarioLoginFormulario

from django.contrib.auth.models import User




def registro(request):
    if request.method=='POST':
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    contexto=  { 'form' : form }
    return render(request, 'registro.html', contexto)


def Home(request):
    borrar_respuestas = PreguntasRespondidas.objects.all()
    borrar_respuestas.delete()
    return render(request,"home.html",{})

def nosotros(request):
    return render(request, "nosotros.html",{})


def loginView(request):
    form = UsuarioLoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect("home")

    contexto = {'form':form}

    return render(request,"login.html",contexto)


# Logout viene por defecto con django.contrib.auth, y el simple hecho de 'ejecutarlo' ya hace logout del usuario
def logoutView(request):
    logout(request)
    return redirect("inicio")

def tablero(request):
    total_usuarios_quiz = UsuarioTrivia.objects.order_by('-puntaje_total')[:10]
    contador = total_usuarios_quiz.count()
    
    context = {

        'usuario_quiz': total_usuarios_quiz,
        'contar_usuario': contador
    }
    return render(request, 'tablero.html', context)


def jugar(request):
    
    #si el usuario ingresa a jugar.html, se crea un UsuarioTrivia, si ya está creado lo obtiene
    UserTrivia, created = UsuarioTrivia.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
	    pregunta_pk = request.POST.get('pregunta_pk')
	    pregunta_respondida = UserTrivia.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
	    respuesta_pk = request.POST.get('respuesta_pk')

	    try:
	    	opcion_selecionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
	    except ObjectDoesNotExist:
	    	raise Http404

	    UserTrivia.validar_intento(pregunta_respondida, opcion_selecionada)

	    return redirect('resultado', pregunta_respondida.pk)

    else:
    	pregunta = UserTrivia.obtener_nuevas_preguntas()
    	if pregunta is not None:
    		UserTrivia.crear_intentos(pregunta)

    	contexto = {
			'pregunta':pregunta
		}
    return render(request,'jugar.html', contexto)

def resultado_pregunta(request, pregunta_respondida_pk):
    respondida = get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)

    contexto = {
        'respondida':respondida
    }
    return render(request,'resultados.html', contexto)


# def prueba(request):
#     usuarios = User.objects.all()
#     return render(request,"home.html",usuarios)
