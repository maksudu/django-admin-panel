from __future__ import unicode_literals
from django.db import models
from hashids import Hashids

SECRET_KEY = '(0%gm^z6s2&y4h^m_vvcq+m7_vl*meg+yggy6@g)!1i_b2o9q_'
hashids = Hashids(salt=SECRET_KEY, min_length=20)
# Create your models here.
class Userrole(models.Model):
    userrole_type = (
        ('1', 'Head Office'),
        ('2', 'Branch'),
        ('3', 'MTO'),
        ('4', 'Agent'),
    )
    user_role_type = models.CharField(max_length=100, choices=userrole_type, null=True, blank=True)
    name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_encoded_id(self):
        return hashids.encrypt(self.id)

class User(models.Model):
    ACTIVE_CHOICES = (
        ('1', 'Active'),
        ('2', 'Inactive'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)
    filename_upload = models.FileField(upload_to="upload/", blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=100)
    userrole = models.ForeignKey(Userrole, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.CharField(max_length=1, default=0, choices=ACTIVE_CHOICES)
    activation_code = models.CharField(max_length=10)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)
    recovery_token=models.CharField(max_length=100)
    recovery_token_time= models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.username

    def get_encoded_id(self):
        return hashids.encrypt(self.id)

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    component = models.CharField(max_length=30)
    action = models.CharField(max_length=20)
    login_data = models.CharField(max_length=300, null=True)
    logout_data = models.CharField(max_length=300, null=True)
    date_time = models.DateTimeField()
    ip = models.GenericIPAddressField()

class Functionname(models.Model):
    module_type = models.CharField(max_length=300, null=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.module_type
    def get_encoded_id(self):
        return hashids.encrypt(self.id)


class Modulename(models.Model):
    module_type = models.ForeignKey(Functionname, on_delete=models.CASCADE,null=True, blank=True)
    module_name = models.CharField(max_length=300, null=True, blank=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.module_name
    def get_encoded_id(self):
        return hashids.encrypt(self.id)

class Moduleurl(models.Model):
    module_type = models.ForeignKey(Functionname, on_delete=models.CASCADE, null=True, blank=True)
    module = models.ForeignKey(Modulename, on_delete=models.CASCADE)
    url = models.CharField(max_length=300, null=True, blank=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.module_name

    def get_encoded_id(self):
        return hashids.encrypt(self.id)

class Privileged(models.Model):
    module = models.ForeignKey(Modulename, on_delete=models.CASCADE)
    moduleurl = models.ForeignKey(Moduleurl, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    userrole = models.ForeignKey(Userrole, on_delete=models.CASCADE)
    module_type =  models.ForeignKey(Functionname, on_delete=models.CASCADE,null=True, blank=True)
    user_role_type = models.IntegerField(null=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)
