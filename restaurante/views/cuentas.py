from django.shortcuts import render


def  agregarCuentas(request, id):
    return render(request, 'pages/cuentas/agregarCuentas.html')