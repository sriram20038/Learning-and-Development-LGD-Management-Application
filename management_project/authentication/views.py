from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .forms import Login_form,Signup_form
from .models import User

def login_view(request):
    form = Login_form()
    if request.method == 'POST':
        form = Login_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id  # Store user session
                    return redirect(f"{user.role.role_name}", user_id=user.id)
                else:
                    form.add_error('password', "Invalid password.")
            except User.DoesNotExist:
                form.add_error('email', "Invalid email or password.")
    
    return render(request, 'authentication/login.html', {'form': form})

def signup_view(request):
    if request.method=='POST':
        form=Signup_form(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            cpassword=form.cleaned_data['confirm_password']
            email = form.cleaned_data['email']
            if password==cpassword:
                form.save()
                return redirect('login')
            else:
                form.add_error(None, "password and confirm password doesnot match")
    else:
        form=Signup_form
    return render(request,'authentication/signup.html',{'form':form})