from django.shortcuts import render
from django.views.generic import CreateView, View, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


# Create your views here.
class SignupView(TemplateView):
    # model = User
    template_name = 'authentication/signup.html'

    def post(self, request):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)

        if email:
            try:
                print('email does not exist')
            except MultipleObjectsReturned:
                return render(request, self.template_name, {'validation_error': 'Email exists. Please use new email'})

        try:
            User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
        except:
            return render(request, self.template_name, {'username_error': 'Username exists. Please use another username'})

        return redirect('authentication:login')
