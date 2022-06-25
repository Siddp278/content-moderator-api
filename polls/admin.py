from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser, text_table
from .forms import UserChangeForm, UserCreationForm

# Configuring the UI of admin page
class UserAdminConfig(UserAdmin):

    model = NewUser
    forms = UserChangeForm   
    add_form = UserCreationForm
     
    # ordering =('-start_date') - this is for listing the data on admin 
    # page with sorting on the basis of start_date, if saved as a value in db
    list_display = ('username', 'is_active')
    # display is for the list not individual users.
    search_fields = ['username', 'is_superuser', 'is_active']

    # To show which fields can be filled/updated for individual user
    fieldsets = (
        ('User Details', {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_superuser' ,'is_staff', 'is_active')}),
    )
    # for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'is_superuser', 'is_staff', 'is_active'),}),)



# Register your models here.
admin.site.register(NewUser, UserAdminConfig)
admin.site.register(text_table)