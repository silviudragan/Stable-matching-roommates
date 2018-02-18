import MySQLdb
from django.db.backends import mysql
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm
from django.views.generic import View
from django.contrib.auth import authenticate, login


def index(request):
    context = {
        'salut': "Buna ziua"
    }
    return render(request, 'stable/index.html', context)


class Login(View):
    form_class = LoginForm
    template_name = 'stable/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST.get('nr_matricol', '')
        password = request.POST.get('parola', '')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'stable/index.html')
        else:
            return render(request, 'stable/login.html')


class UserFormView(View):
    form_class = UserForm
    template_name = 'stable/register.html'

    def get(self, request):
        form = self.form_class(None)
        studenti = ""
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        re_password = request.POST.get('re_password', '')
        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if password != re_password:
                return render(request, self.template_name, {'form': form})
            conn = MySQLdb.connect(host="localhost",
                                 user="root",
                                 passwd="Silviu01",
                                 db="test")
            c = conn.cursor()
            c.execute("SELECT * FROM stable_student")
            studenti = c.fetchall()
            # verificam daca numarul matricol este valid
            id_valid = False
            for student in studenti:
                if username in student:
                    id_valid = True

            if not id_valid:
                return render(request, self.template_name, {'form': form, 'mesaj': "Numarul matricol nu este valid."})

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
        return render(request, self.template_name, {'form': form})
