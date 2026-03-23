from django.shortcuts import render, redirect
from .models import User, SavedPassword
import string
import random

# LOGIN
def login_page(request):
    if request.method == "POST":
        name = request.POST.get("username")
        pw = request.POST.get("password")

        try:
            user = User.objects.get(username=name, password=pw)
            request.session["user"] = user.username
            return redirect("/dashboard/")
        except:
            return render(request, "login.html", {"error": "Falsche Daten"})

    return render(request, "login.html")


# REGISTER
def register_page(request):
    if request.method == "POST":
        name = request.POST.get("username")
        pw = request.POST.get("password")

        User.objects.create(username=name, password=pw)

        return redirect("/")

    return render(request, "register.html")


# DASHBOARD
def dashboard_page(request):
    if "user" not in request.session:
        return redirect("/")
    return render(request, "dashboard.html")


# PASSWORT PRÜFEN
def check_page(request):
    if "user" not in request.session:
        return redirect("/")

    score = 0
    text = ""
    tips = []

    if request.method == "POST":
        pw = request.POST.get("pw")

        if len(pw) > 6:
            score += 2
        else:
            tips.append("Passwort länger als 6 Zeichen machen")

        if len(pw) > 10:
            score += 2

        if any(char.isdigit() for char in pw):
            score += 2
        else:
            tips.append("Zahlen hinzufügen")

        if any(char.isupper() for char in pw):
            score += 2
        else:
            tips.append("Großbuchstaben verwenden")

        if any(char in string.punctuation for char in pw):
            score += 2
        else:
            tips.append("Sonderzeichen benutzen (!, ?, %, @, ...)")

        if score <= 4:
            text = "Passwort ist schwach"
        elif score <= 7:
            text = "Passwort ist mittel"
        else:
            text = "Passwort ist stark"

        return render(request, "check.html", {
            "score": score,
            "text": text,
            "tips": tips
        })

    return render(request, "check.html")


# PASSWORT GENERIEREN (NEUE VERSION)
def generate_page(request):
    if "user" not in request.session:
        return redirect("/")

    pw = ""

    if request.method == "POST":
        length = int(request.POST.get("length"))

        chars = ""

        if request.POST.get("lower"):
            chars += string.ascii_lowercase
        if request.POST.get("upper"):
            chars += string.ascii_uppercase
        if request.POST.get("digits"):
            chars += string.digits
        if request.POST.get("symbols"):
            chars += "!$%&/()=?@#*"

        if chars == "":
            pw = "Bitte Optionen auswählen!"
        else:
            pw = "".join(random.choice(chars) for _ in range(length))

    return render(request, "generate.html", {"pw": pw})


# PASSWÖRTER SPEICHERN
def mypasswords_page(request):
    if "user" not in request.session:
        return redirect("/")

    if request.method == "POST":
        pw = request.POST.get("pw")
        note = request.POST.get("note")

        SavedPassword.objects.create(text=pw, note=note)

    all_pw = SavedPassword.objects.all()

    return render(request, "mypasswords.html", {"passwords": all_pw})


# PASSWORT LÖSCHEN
def delete_password(request, id):
    if "user" not in request.session:
        return redirect("/")

    try:
        pw = SavedPassword.objects.get(id=id)
        pw.delete()
    except:
        pass

    return redirect("/mypasswords/")


# LOGOUT
def logout_page(request):
    try:
        del request.session["user"]
    except:
        pass

    return redirect("/")
