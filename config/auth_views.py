from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .access_control import ensure_roles_exist


def login_view(request):
    ensure_roles_exist()

    if request.user.is_authenticated:
        return redirect("dashboard")
    
    error_messsage = None

    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user =  authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        
        error_messsage = "Usuário ou senha inválidos."

    return render(request, "auth/login.html", {"error_message": error_messsage})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")