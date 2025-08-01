import os
import shutil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def respaldar_db(request):
    try:
        # BASE_DIR apunta al nivel de manage.py
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))

        origen = os.path.join(BASE_DIR, 'restaurante.db')
        destino = r"C:\Users\jaire\OneDrive\Respaldos\restaurante.db"
        destino_dir = os.path.dirname(destino)

        if not os.path.exists(origen):
            return JsonResponse({'status': 'error', 'message': f'No se encontró el archivo: {origen}'})

        os.makedirs(destino_dir, exist_ok=True)
        shutil.copy2(origen, destino)

        return JsonResponse({'status': 'success', 'message': 'Base de datos copiada exitosamente a OneDrive'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
