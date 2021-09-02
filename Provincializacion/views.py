from django.shortcuts import render



# Create your views here.

def inicio(request):

    saludo = "Bienvenidos"

    return render(request,"inicio.html",{"holiwis":saludo})

