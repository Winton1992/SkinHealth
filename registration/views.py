from django.shortcuts import render,redirect
# from registration.forms import RegistrationForm,EditProfileForm
# from django.contrib.auth.models import User
# from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import RegistrationForm,EditProfileForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied



def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/auth/login/')
    else:
        form=RegistrationForm()

        args={'form':form}
        return render(request,'reg_form.html',args)

def view_profile(request):
     args = {'user': request.user}
     return render(request, 'profile.html', args)


@login_required() # only logged in users should access this
def edit_user(request):

    user_form = EditProfileForm(instance=request.user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('gender','skinType'))
    formset = ProfileInlineFormset(instance=request.user)

    if request.user.is_authenticated():
        if request.method == "POST":
            user_form =EditProfileForm(request.POST, request.FILES, instance=request.user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=request.user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/registration/profile/')

        return render(request, "update_user.html",{
            "noodle": request.user.id,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
