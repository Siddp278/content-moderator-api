# https://www.youtube.com/watch?v=Ae7nc1EGv-A
# Run python manage.py <command> --dry-run to check if things are working porperly.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from string import ascii_letters, digits
from secrets import choice


def password_gen():
    alphabet = ascii_letters + digits
    rand_password = ''.join(choice(alphabet) for i in range(8))
    return(rand_password)


class CustomAccountManager(BaseUserManager):

    def create_user(self, username, password=None, **other_fields):
        
        if username == None:
            raise ValueError('You must provide an username properly.')

        # other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_staff', True)   
        other_fields.setdefault('is_active', True) 
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save(using= self._db)
        return user

    def create_superuser(self, username, password=None, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must beassigned to is_superuser=True')

        user = self.create_user(username, **other_fields)
        user.set_password(password)
        user.save(using= self._db)

        return user   

    def create_user_without_pass(self, username):
        # cant create a superuser with this method.
        password = password_gen()
        self.create_user(username, password)
        return password         



class NewUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=500)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password'] # dont include username here since we provided it inside USERNAME_FIELD


    def __str__(self):
        return self.username




class text_table(models.Model):
    text = models.CharField(max_length=2000)
    label = models.CharField(max_length=50, default='no input')
    predicted = models.CharField(max_length=50, default='no input')
    lang = models.CharField(max_length=10, default='en')
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    text_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)    