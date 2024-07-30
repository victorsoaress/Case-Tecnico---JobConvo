from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

def empresa_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Verifique se o usuário está autenticado
        
        if not request.user.is_authenticated:
            return redirect('login')  # Redirecione para a página de login, ajuste a URL conforme necessário
        user = request.user
        # Verifique o tipo de usuário
        if user.groups.filter(name='candidato').exists():
            raise PermissionDenied  # Ou redirecione para uma página de erro ou outra página

        return view_func(request, *args, **kwargs)

    return _wrapped_view