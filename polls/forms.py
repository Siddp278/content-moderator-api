from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import NewUser

# UserCreationForm and UserChangeForm created so that we can add/update user data in admin page also.

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label = 'Password' , widget = forms.PasswordInput)
    # password2 = forms.CharField(label = 'Confirm Password' , widget = forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ('username', 'is_superuser', 'is_staff', 'is_active')

    #IF YOU GET ANY TYPE OF ERROR TRY CHANGING THIS
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     return password1
    
    # Save the provided password in hashed format
    def save(self, commit = True):
        user = super(UserCreationForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if(commit):
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NewUser
        fields = ('id', 'username', 'is_superuser', 'is_staff', 'is_active')
    
    def clean_password(self):
        return self.initial["password"]