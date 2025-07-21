from django.shortcuts import render
from ..models import Mesas

def listarCocinas(request):
    # Render the template with the list of kitchens
    return render(request, 'pages/cocinas/listarCocinas.html')