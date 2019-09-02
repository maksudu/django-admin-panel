from django import forms
from usermanagement.models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('recovery_token','recovery_token_time','activation_code', 'last_name', 'created_at', 'created_by_id', 'modified_by', 'modified_by_id',)
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "password": forms.TextInput(attrs={'class': 'form-control','type': 'password'}),
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.Textarea(attrs={'class': 'form-control'}),
            "userrole": forms.Select(attrs={'class': 'form-control'}),
            "is_active": forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            "first_name": "Name",
            "username": "User Id",
            "filename_upload":"Picture upload",
        }


class UserFormMTO(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=20, widget=forms.TextInput(attrs={'type': 'password'}))
    first_name = forms.CharField(max_length='50', label='Name')

    class Meta:
        model = User
        fields = '__all__'
        exclude = (
            'transfercompany', 'branch_name', 'activation_code', 'last_name', 'created_at', 'created_by_id',
            'modified_by',
            'modified_by_id',)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('recovery_token','recovery_token_time','password', 'activation_code', 'last_name', 'created_at', 'created_by_id', 'modified_by', 'modified_by_id',)
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.Textarea(attrs={'class': 'form-control'}),
            "userrole": forms.Select(attrs={'class': 'form-control'}),
            "is_active": forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            "first_name": "Name",
            "username": "User Id",
        }



class UserEditFormMTO(forms.ModelForm):
    # password = forms.CharField(label='Password',max_length =20, widget=forms.TextInput(attrs={'type': 'password'}))
    first_name = forms.CharField(max_length='50', label='Name')

    class Meta:
        model = User
        fields = '__all__'
        exclude = (
            'password', 'transfercompany', 'branch_name', 'activation_code', 'last_name', 'created_at', 'created_by_id',
            'modified_by', 'modified_by_id',)


class ChangePasswordForm(forms.Form):
    # old_password = forms.CharField(label = 'Old Password', widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))
    new_password = forms.CharField(label='New Password', min_length=6,
                                   widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}))

    def __init__(self, user=None, data=None, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(data=data, *args, **kwargs)


class PasswordResetForm(forms.Form):
	new_password = forms.CharField(label = 'New Password', min_length = 6, widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))
	confirm_password = forms.CharField(label = 'Confirm Password', widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))

	def clean_confirm_password(self):
		new_password =  self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if new_password!=confirm_password:
			raise forms.ValidationError("Passwords don't match")
		return new_password

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))

    def clean(self):
        cleaned_data = super(EmailForm, self).clean()
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if not user:
            raise forms.ValidationError("Can't find that email, sorry.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length='50', label='User Id')
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={'type': 'password'}))


class UserroleForm(forms.ModelForm):
    class Meta:
        model = Userrole
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "user_role_type": forms.Select(attrs={'class': 'form-control'}),
        }


class PrivilegedForm(forms.ModelForm):
    class Meta:
        model = Privileged
        exclude = ('url', 'created_by_id', 'modified_by_id', 'created_at', 'modified_by',)


class ModuleurlForm(forms.ModelForm):
    class Meta:
        model = Moduleurl
        fields = '__all__'
        widgets = {
            "url": forms.TextInput(attrs={'class': 'form-control'}),
            "module_type": forms.Select(attrs={'class': 'form-control'}),
            "module": forms.Select(attrs={'class': 'form-control'}),
        }
        exclude = ('created_by_id', 'modified_by_id', 'created_at', 'modified_by',)