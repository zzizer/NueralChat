from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import CustomUserUpdateForm
from django.contrib.auth.decorators import login_required


def signin(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('new_chat')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')

    return render(request, 'accounts_mgt/signin.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        else:

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('signup')
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            else:
                user = CustomUser.objects.create_user(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('signin')

    return render(request, 'accounts_mgt/signup.html')

def signout(request):
    logout(request)
    return redirect('welcome_page')

@login_required(login_url='signin')
def profile(request, id):
    user = request.user

    profile = CustomUser.objects.get(id=id)

    context = {'user': user, 'profile': profile}

    return render(request, 'accounts_mgt/profile.html', context)

class EditProfile(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'accounts_mgt/edit_profile.html'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.kwargs['id'])

    def get_success_url(self):
        user_id = self.object.id
        return reverse_lazy('profile', kwargs={'id': user_id})