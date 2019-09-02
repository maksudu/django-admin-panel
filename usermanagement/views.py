from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
import hashlib
from django.utils import timezone
import datetime, time
from datetime import datetime
from .decorators import access_permission_required, login_required
from Crm.utils import get_decoded_id, get_encoded_id
from .forms import *
from django.core.mail import send_mail, BadHeaderError
from dateutil.relativedelta import relativedelta


# Create your views here.
def login(request):
    if 'logged_in' in request.session:
        if request.session['logged_in'] is True:
            return redirect('usermanagement:dashboard')
    else:
        form = LoginForm
        return render(request, 'usermanagement/login.html', {'form': form})


def login_validate(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        pasw = form['password'].value().encode('utf-8')
        password = hashlib.sha1(pasw).hexdigest()
        username = form['username'].value()
        try:
            user = User.objects.get(username=username)
        except:
            user = None

        if user is None:
            messages.error(request, 'Username Mismatch!')
            return redirect('usermanagement:login')
        else:
            if user.password == password:
                if user.is_active == '1':
                    request.session['logged_in'] = True
                    request.session['username'] = user.username
                    request.session['id'] = user.pk
                    Log.objects.create(
                        user_id=request.session['id'],
                        date_time=datetime.now(),
                        login_data=datetime.now(),
                        action='1',
                        ip=request.META.get('REMOTE_ADDR')
                    )

                    return redirect("usermanagement:dashboard")

                else:
                    messages.error(request, 'Your Account is not active. Please contact Admin.')
                    return redirect('usermanagement:login')
            else:
                messages.error(request, 'Incorrect Password!')
                return redirect('usermanagement:login')
    else:
        return render(request, 'usermanagement/login.html', {'form': form})


@login_required("logged_in", 'usermanagement:login')
def dashboard(request):
    module = list()
    user = User.objects.get(id=request.session['id'])
    user_permissions = Privileged.objects.filter(userrole_id=user.userrole_id)
    module = Privileged.objects.filter(userrole_id=user.userrole_id).values('module_type_id').distinct()
    list_result = [entry for entry in module]
    request.session['module'] = list_result
    try:
        urls = list()
        for p in user_permissions:
            userurl = Moduleurl.objects.filter(id=p.moduleurl_id)
            for url in userurl:
                urls.append(url.url)
                request.session['urls'] = urls
    except:
        user = None

    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': urls,
        'module': module,

    }
    context = {
        'data': userdata,

    }
    return render(request, 'usermanagement/dashboard.html', context)


@login_required("logged_in", 'usermanagement:login')
def logout(request):
    try:
        user_log = Log.objects.filter(user_id=request.session['id']).last()
        user_log.logout_data = datetime.now()
        user_log.save()
        del request.session['logged_in']
    except:
        user_log.save()

    return redirect('usermanagement:login')


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def User_list(request):
    # if 'logged_in' in request.session:
    #     if request.session['logged_in'] is True:
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    user = User.objects.all()

    context = {
        'data': userdata,
        'user': user,
    }

    return render(request, 'usermanagement/user_list.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def User_data_form(request):
    form = UserForm
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    context = {
        'data': userdata,
        'form': form,
    }

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES or None)
        pasw = form['password'].value().encode('utf-8')
        password = hashlib.sha1(pasw).hexdigest()
        existinguser = User.objects.filter(username=request.POST['username'])
        if existinguser:
            messages.error(request, 'Duplicate Username Exists')
            return redirect('usermanagement:User_data_form')
        else:
            form = form.save(commit=False)
            form.created_by_id = request.session['id']
            form.created_at = datetime.now()
            form.save()
            messages.success(request, 'Data Successfully Saved')

        return redirect('usermanagement:User_list')

    else:
        context = {
            'data': userdata,
            'form': form,
        }
    return render(request, 'usermanagement/user_add.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def user_data_edit(request, pk):
    master_data = get_object_or_404(User, pk=get_decoded_id(pk))
    userrole = Userrole.objects.all()
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    data = {
        'first_name': master_data.first_name,
        'email': master_data.email,
        'phone': master_data.phone,
        'username': master_data.username,
        'address': master_data.address,
        'is_active': master_data.is_active,
        'userrole': master_data.userrole,
    }
    form = UserEditForm(data)
    context = {
        'data': userdata,
        'form': form,
        'userrole': userrole,
        'id': master_data.pk,
    }
    if request.method == 'POST':
        master_data = get_object_or_404(User, pk=get_decoded_id(pk))
        form = UserEditForm(request.POST or None)
        form = UserEditForm(request.POST, instance=master_data)
        if form.is_valid():
            form.modified_by = datetime.now()
            form.modified_by_id = request.session['id']
            form.save()
            messages.success(request, 'Data Successfully Updated')
        return redirect('usermanagement:User_list')
    return render(request, 'usermanagement/user_add.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def user_data_delete(request, pk):
    if request.session['id'] == get_decoded_id(pk):
        messages.error(request, 'Can not delete')
        return redirect('usermanagement:User_list')
    else:
        User.objects.get(pk=get_decoded_id(pk)).delete()
        messages.success(request, 'Data Delete')
        return redirect('usermanagement:User_list')


@login_required("logged_in", 'usermanagement:login')
def User_profile(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    userprofile = User.objects.get(id=request.session['id'])

    context = {
        'data': userdata,
        'userprofile': userprofile,
    }

    return render(request, 'usermanagement/user _profile.html', context)


def change_password(request, pk):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    user = get_object_or_404(User, pk=get_decoded_id(pk))
    form = ChangePasswordForm(user=request.user, data=request.POST or None)
    contex = {
        'data': userdata,
        'form': form,
        'next': next,
        'id': pk,
    }
    return render(request, 'usermanagement/change_password.html', contex)


def reset_password(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    id = request.POST['id']
    changepassword = request.POST['new_password']
    password = hashlib.sha1(changepassword.encode('utf-8')).hexdigest()
    master_data = get_object_or_404(User, pk=get_decoded_id(id))
    User.objects.filter(id=master_data.id).update(password=password)
    messages.success(request, 'Password Changes Updated')
    return redirect('usermanagement:User_list')
    contex = {
        'data': userdata,
    }
    return render(request, 'usermanagement/change_password.html', contex)


def forget_password(request):
    return render(request, 'usermanagement/forget_password.html')


def forget_password_email(request):
    form = EmailForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = get_encoded_id(round(time.time() * 1000))
            user.recovery_token = token
            user.save()
            try:
                send_mail("Reset Password", "Access Code:" + token, 'Admin', [email])

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return render(request, 'usermanagement/send_email_success.html')

    return render(request, 'usermanagement/change_password.html', {'form': form})


def Access_code(request):
    users = User.objects.get(recovery_token=request.POST['recovery_token'])
    id=users.id

    if not users:
        messages.error(request, "Your access code mismatch. Please try again")
        return render(request, 'usermanagement/send_email_success.html')
    else:
        form = PasswordResetForm(request.POST or None)
    contex = {
        'id': id,
        'form': form,
    }
    return render(request, 'usermanagement/reset_password.html', contex)

def New_password(request):
    print(request.POST)
    if request.method == 'POST':
        id = request.POST['id']
        changepassword = request.POST['new_password']
        password = hashlib.sha1(changepassword.encode('utf-8')).hexdigest()
        master_data = get_object_or_404(User, pk=get_decoded_id(id))
        User.objects.filter(id=master_data.id).update(password=password)
        messages.success(request, 'Password Changes Updated')
        return render(request, 'usermanagement/login.html')
    return render(request, 'usermanagement/reset_password.html')

# user role start  function

@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def Userrole_list(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    userrole = Userrole.objects.all()

    context = {
        'data': userdata,
        'userrole': userrole,
    }

    return render(request, 'usermanagement/userrole_list.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def Userrole_data_form(request):
    form = UserroleForm
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    context = {
        'data': userdata,
        'form': form
    }

    if request.method == 'POST':
        form = UserroleForm(request.POST, request.FILES or None)
        if form.is_valid():
            process_area = form.save(commit=False)
            process_area.save()
            messages.success(request, 'Data Successfully Saved')
            return redirect('usermanagement:Userrole_list')
        else:
            context = {
                'data': userdata,
                'form': form
            }
            return render(request, 'usermanagement/userrole_add.html', context)
    return render(request, 'usermanagement/userrole_add.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def userrole_data_edit(request, pk):
    master_data = get_object_or_404(Userrole, pk=get_decoded_id(pk))
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    data = {
        'name': master_data.name,
        'description': master_data.description,
        'user_role_type': master_data.user_role_type,
    }
    form = UserroleForm(data)
    context = {
        'data': userdata,
        'form': form,
        'id': master_data.pk,
    }
    if request.method == 'POST':
        master_data = get_object_or_404(Userrole, pk=get_decoded_id(pk))
        form = UserroleForm(request.POST or None)
        if request.method == 'POST':
            form = UserroleForm(request.POST, instance=master_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Updated')

        return redirect('usermanagement:Userrole_list')
    return render(request, 'usermanagement/userrole_add.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def userrole_data_delete(request, pk):
    userrole = get_object_or_404(Userrole, pk=get_decoded_id(pk))
    userrole.delete()
    messages.success(request, 'Data Delete')
    return redirect('usermanagement:Userrole_list')


@login_required("logged_in", 'usermanagement:login')
def Privillage_list(request, id, user_role_type):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    modulelists = list()
    modulelall = list()

    privileged = Privileged.objects.filter(userrole_id=id).order_by('module_id')

    if privileged.count() == 0:
        modulelall = Modulename.objects.all()
        moduleurl = Moduleurl.objects.all()
    else:
        modulelall = Modulename.objects.all()
        moduleurl = Moduleurl.objects.all()

    context = {
        'data': userdata,
        'modulelall': modulelall,
        'id': id,
        'userrole_id': id,
        'user_role_type': user_role_type,
        'privileged': privileged,
        'modulelists': modulelists,
        'moduleurl': moduleurl,
    }

    return render(request, 'usermanagement/Privillage_list.html', context)


# @access_permission_required
def add_role_with_permission(request):
    form = PrivilegedForm
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],
    }
    context = {
        'data': userdata,
        'form': form
    }
    if request.method == 'POST':
        list = request.POST.getlist('list')
        user_id = request.POST['user_id']
        userrole_id = request.POST['userrole_id']
        user_role_type = request.POST['user_role_type']
        Privileged.objects.filter(userrole_id=userrole_id).delete()
        for id in list:
            id = id.split(',')
            Privileged.objects.create(moduleurl_id=id[0], module_id=id[1], module_type_id=id[2],
                                      userrole_id=userrole_id, user_role_type=user_role_type,
                                      created_by_id=user_id, created_at=datetime.now())
        messages.success(request, 'Data Saved  Successfully')
        return redirect('usermanagement:Userrole_list')
    else:
        context = {
            'data': userdata,
            'form': form
        }
    return render(request, 'usermanagement/privillage_add.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def moduleurl_list(request):
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    url = Moduleurl.objects.all()

    context = {
        'data': userdata,
        'url': url,
    }

    return render(request, 'usermanagement/moduleurl_list.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def moduleurl_data_form(request):
    form = ModuleurlForm
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    context = {
        'data': userdata,
        'form': form
    }

    if request.method == 'POST':
        form = Moduleurl(request.POST, request.FILES or None)
        if form.is_valid():
            process_area = form.save(commit=False)
            process_area.save()
            messages.success(request, 'Data Successfully Saved')
            return redirect('usermanagement:moduleurl_list')
        else:
            context = {
                'data': userdata,
                'form': form
            }
            return render(request, 'usermanagement/moduleurl_add.html', context)
    return render(request, 'usermanagement/moduleurl_add.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def moduleurl_data_edit(request, pk):
    master_data = get_object_or_404(Moduleurl, pk=get_decoded_id(pk))
    userdata = {
        'user_id': request.session['id'],
        'username': request.session['username'],
        'urls': request.session['urls'],

    }
    data = {
        'url': master_data.url,
        'module_type': master_data.module_type,
        'module': master_data.module,

    }
    form = ModuleurlForm(data)
    context = {
        'data': userdata,
        'form': form,
        'id': master_data.pk,
    }
    if request.method == 'POST':
        master_data = get_object_or_404(Moduleurl, pk=get_decoded_id(pk))
        form = ModuleurlForm(request.POST or None)
        if request.method == 'POST':
            form = ModuleurlForm(request.POST, instance=master_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Updated')

        return redirect('usermanagement:moduleurl_list')
    return render(request, 'usermanagement/moduleurl_add.html', context)


@login_required("logged_in", 'usermanagement:login')
@access_permission_required
def moduleurl_data_delete(request, pk):
    url = get_object_or_404(Moduleurl, pk=get_decoded_id(pk))
    url.delete()
    messages.success(request, 'Data Delete')
    return redirect('usermanagement:moduleurl_list')
