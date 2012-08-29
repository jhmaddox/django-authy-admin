from django.contrib import admin
from django.contrib.admin.models import User

class AuthyAdminUserAdmin(admin.ModelAdmin):

    """
    AuthyAdminUserAdmin configures the AuthyAdminUser list view to show
    all fields as columns and to limit user dropdown to staff members

    """

    list_display = ['user', 'authy_id', 'country_code', 'phone_number']
    readonly_fields = ['authy_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        """
        limits user choices to staff members

        """

        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_staff=True)

        return (super(AuthyAdminUserAdmin, self)
                .formfield_for_foreignkey(db_field, request, **kwargs))


