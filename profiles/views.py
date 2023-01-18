from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.decorators import login_required
from helpers.decorators import auth_user_should_not_access
from django.contrib import messages
# from .models import Userprofile

from django.utils.text import slugify
from store.forms import  ImageForm, PropertyForm
from store.models import Property, Image
# Create your views here.




def agent_profile(request, username):
    user = User.objects.get(username=username)
    properties = Property.objects.filter(user=user).exclude(status=Property.DELETED)

    context = {
        'user': user,
        'properties': properties,
    }
    return render(request, 'profiles/agent_profile.html', context)




@login_required
def add_property(request):
    propertyform = PropertyForm()
    imageform = ImageForm()

    if request.method =='POST':
        files = request.FILES.getlist('images')

        propertyform = PropertyForm(request.POST, request.FILES)
        if propertyform.is_valid():
            title = request.POST.get('title')
            property = propertyform.save(commit=False)
            property.slug = slugify(title)
            property.user = request.user
            property.save()

            for file in files:
                Image.objects.create(property=property, images=file)
                messages.add_message(request, messages.SUCCESS,
                             'Property listed')
            return redirect('agent_profile', username=request.user.username )
    context = {
        'p_form': propertyform,
        'i_form': imageform,
    }



    return render(request, 'profiles/property_form.html', context)


@login_required
def edit_property(request, id):
    property = Property.objects.filter(user=request.user).get(id=id)
   
    

    propertyform = PropertyForm(instance=property)
    imageform = ImageForm()

    if request.method =='POST':
        files = request.FILES.getlist('images')

        propertyform = PropertyForm(request.POST, request.FILES, instance=property)
        if propertyform.is_valid():
            property = propertyform.save(commit=False)
            property.save()

            for file in files:
                Image.objects.update_or_create(property=property, images=file)
            messages.add_message(request, messages.SUCCESS,
                             'Property updated')
            return redirect('agent_profile', username=request.user.username)

       
    context = {
        'p_form': propertyform,
        'i_form': imageform,
    }
    return render(request, 'profiles/property_form.html', context)


@login_required
def delete_property(request, id):
    property = Property.objects.filter(user=request.user).get(id=id)
    property.status = Property.DELETED
   
    property.save()

    messages.add_message(request, messages.SUCCESS,
                             'Property deleted')

    return redirect('agent_profile', username=request.user.username)


@auth_user_should_not_access
def register(request):
    if request.method == 'POST':
        context = {
            'has_error': False, 
            'data': request.POST
        }
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number =  request.POST.get('phone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')


        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
            'password should be at least 6 character')
            context['has_error'] = True
        
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch')
            context['has_error'] = True

        # if not validate_email(email):
        #     messages.add_message(request, messages.ERROR,
        #                          'Enter a valid email address')
        #     context['has_error'] = True

        if not first_name:
            messages.add_message(request, messages.ERROR,
                                 'name is required')
            context['has_error'] = True
            return render(request, 'profiles/signup.html', context, status=409)


        if not last_name:
            messages.add_message(request, messages.ERROR,
                                 'name is required')
            context['has_error'] = True
            return render(request, 'profiles/signup.html', context, status=409)
            

        if not phone_number:
            messages.add_message(request, messages.ERROR,
                                 'phone number  is required')
            context['has_error'] = True

        if User.objects.filter(phone_number=phone_number).exists():
            messages.add_message(request, messages.ERROR,
                                 'phone number is taken, choose another one')
            context['has_error'] = True

            return render(request, 'profiles/signup.html', context, status=409)


        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username is taken, choose another one')
            context['has_error'] = True

            return render(request, 'profiles/signup.html', context, status=409)

     
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is taken, choose another one')
            context['has_error'] = True

            return render(request, 'profiles/signup.html', context, status=409)

        if context['has_error']:
            return render(request, 'profiles/signup.html', context)

        

        user = User.objects.create_user(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            phone_number=phone_number, 
            email=email)
        user.set_password(password)
        user.save()
        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f'welcome {user.username}')

        return redirect('agent_profile', username=request.user.username)


        


        # if not context['has_error']:

        #     send_activation_email(user, request)

        #     messages.add_message(request, messages.SUCCESS,
        #                          'We sent you an email to verify your account')
            # return redirect('login')
    return render(request, 'profiles/signup.html')



@auth_user_should_not_access
def login_user(request):

    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

    
        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Invalid credentials, try again')
            return render(request, 'profiles/login.html', context, status=401)

        login(request, user)
        

        messages.add_message(request, messages.SUCCESS,
                             f'Welcome {user.username}')

        return redirect('agent_profile', username=request.user.username)

    return render(request, 'profiles/login.html')



@login_required
def logout_user(request):

    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'Successfully logged out')

    return redirect('frontpage')
