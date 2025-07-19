from django.shortcuts import redirect, render
from django.http import JsonResponse

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout, authenticate
from restaurante.models import Cajas, Usuarios
from django.contrib import messages
from .utils import login_required, logout_required, admin_required, vendedor_required

    # nombre = 'Jair Hernandez'
    # user = 'JairHC'
    # contra = '1234'
    # rol = 1

    # contra_cifrada = make_password(contra)

    # Usuarios.objects.create(
    #     nombre=nombre,
    #     user=user,
    #     contra=contra_cifrada,
    #     rol=rol
    # )


def datosUser(request):
    user = Usuarios.objects.get(pk=request.session['user_id'])
    # notisStock = notificar_stock_bajo()
    # notisVencimiento = notificar_vencimientos()
    
    return {
        'user': user,
        'nombre': user.nombre,
        'userId': user.usuarioid,
        'rolid': user.rol
        # 'notisStock': notisStock,
        # 'notisVencimiento': notisVencimiento,
        # 'numeroNotificaciones': len(notisVencimiento) + len(notisStock),
    }


# Create your views here.
@login_required
def dashboard(request):
    user_data = datosUser(request)
    caja_abierta = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).first()
    if caja_abierta:
        datos = {
            **user_data,
            'hora': caja_abierta.fechaapertura,
            'tiempo': caja_abierta.fechaapertura,
            'caja': caja_abierta,
            
        }
        return render(request, 'dashboard.html', datos)
    return render(request, 'dashboard.html', user_data)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('pass')
        print(f"Username: {username}, Password: {password}")
        
        try:
            user = Usuarios.objects.get(user=username)
            
            if check_password(password, user.contra):
                request.session['user_id'] = user.pk
                
                return redirect('dashboard')
            else:
                return render(request, 'auth/login.html', {'error': 'Credenciales inválidas'})
            
        except Usuarios.DoesNotExist:
            return render(request, 'auth/login.html', {'error': 'Usuario no encontrado'})

        
    else:
        return render(request, 'auth/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')