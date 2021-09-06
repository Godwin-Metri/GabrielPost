from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"You successfully registered as {username} !")
            return redirect('login')

        else:
            print("User not created")
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', context={'form': form})

