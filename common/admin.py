from __future__ import unicode_literals
from common.models import User, Profile, Address
from django.contrib import admin

# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# admin.site.register(MobileOTP)
admin.site.register(Address)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'username', 'first_name', 'last_name', 'get_full_name', 'email', 'mobile', 'role',
                    'date_joined')
    list_filter = ('email', 'role', 'is_staff','is_active' ,'is_admin', )
    '''search_fields = ('mobile', 'first_name', 'last_name')
    ordering = ('mobile', '-is_active')
    filter_horizontal = ()'''
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'email', 'gender', 'role')}),
        ('Permissions', {'fields': ('is_admin','is_staff','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2')}
        ),
    )


    search_fields = ('mobile','first_name', 'last_name')
    ordering = ('mobile','-is_active')
    filter_horizontal = ()
    list_per_page = 10
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, UserAdmin)
