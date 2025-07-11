from django.shortcuts import redirect, render

from apps.administrador.models import Negocio
from apps.servicios.models import Servicio


def pagina_principal(request):
    ''' 
    Muestra la página principal del sitio. Si el usuario está autenticado, 
    redirige a diferentes vistas según su rol. Los usuarios no autenticados 
    ven la página principal con la información del negocio y los servicios disponibles.
    '''
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtiene el rol del usuario
        rol = getattr(request.user, 'rol', None)

        # Redirección según el rol del usuario
        if rol == 'administrador':
            return redirect('configuracion_negocio')
        elif rol == 'dueño':
            return redirect('dashboard')
        elif rol == 'cliente':
            # Si el usuario es cliente, muestra la página principal con negocio y servicios
            negocio = Negocio.objects.first()
            servicios = Servicio.objects.all()
            return render(request, 'pagina_principal.html', {'negocio': negocio, 'servicios': servicios})

    # Para usuarios no autenticados, muestra la página principal con negocio y servicios
    negocio = Negocio.objects.first()
    servicios = Servicio.objects.all()
    return render(request, 'pagina_principal.html', {'negocio': negocio, 'servicios': servicios})



