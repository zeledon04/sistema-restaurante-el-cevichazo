import os
import shutil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sistema.settings import BASE_DIR
db_path = os.path.join(os.environ.get('LOCALAPPDATA', BASE_DIR), 'Restaurante')

@csrf_exempt
def respaldar_db(request):
    try:
        # Ruta original de la base de datos
        origen = os.path.join(db_path, 'restaurante.db')

        # Carpeta del usuario actual
        user_dir = os.path.expanduser("~")

        # Intentar ruta de OneDrive primero
        onedrive_dir = os.path.join(user_dir, 'OneDrive', 'Respaldos')
        # Si no existe, usar Documentos/Respaldos
        if not os.path.exists(onedrive_dir):
            onedrive_dir = os.path.join(user_dir, 'Documents', 'Respaldos')

        os.makedirs(onedrive_dir, exist_ok=True)
        destino = os.path.join(onedrive_dir, 'restaurante.db')

        # Verificar si existe la base de datos original
        if not os.path.exists(origen):
            return JsonResponse({'status': 'error', 'message': f'No se encontró el archivo: {origen}'})

        shutil.copy2(origen, destino)

        return JsonResponse({'status': 'success', 'message': 'Base de datos copiada exitosamente a OneDrive'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
