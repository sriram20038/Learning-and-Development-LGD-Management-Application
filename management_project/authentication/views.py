from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .forms import Login_form,Signup_form
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = Login_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Check if user exists in the database
                user = User.objects.get(email=email)

                # Secure password validation with hashed password
                if check_password(password, user.password):
                    request.session['user_id'] = user.id  # Store the user in the session
                    return redirect(f"{user.role.role_name}")  # Redirect to a success page (e.g., home page)
                else:
                    form.add_error(None, "Invalid password")  # Invalid password error

            except User.DoesNotExist:
                form.add_error(None, "Invalid email or password")  # Invalid email error

    else:
        form = Login_form()

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