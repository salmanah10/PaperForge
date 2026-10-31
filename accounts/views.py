from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

User = get_user_model()


def _back(tab):
    return redirect(f"{reverse('home')}?tab={tab}")


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "home.html", {"tab": request.GET.get("tab", "")})


@require_POST
def register_view(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")
    password2 = request.POST.get("password2", "")

    error = None
    if not name:
        error = "Please enter your full name."
    else:
        try:
            validate_email(email)
        except ValidationError:
            error = "Please enter a valid email address."
    if not error and User.objects.filter(username=email).exists():
        error = "An account with this email already exists. Try signing in."
    if not error and password != password2:
        error = "Passwords do not match."
    if not error:
        try:
            validate_password(password)
        except ValidationError as e:
            error = " ".join(e.messages)

    if error:
        messages.error(request, error)
        return _back("signup")

    user = User.objects.create_user(
        username=email, email=email, password=password, first_name=name
    )
    login(request, user)
    return redirect("dashboard")


@require_POST
def login_view(request):
    identifier = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")

    match = User.objects.filter(email__iexact=identifier).first()
    username = match.username if match else identifier

    user = authenticate(request, username=username, password=password)
    if user is None:
        messages.error(request, "Incorrect email or password.")
        return _back("signin")

    login(request, user)
    if not request.POST.get("remember"):
        request.session.set_expiry(0)
    return redirect("dashboard")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")