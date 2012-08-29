from django.contrib.admin.sites import AdminSite
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache

from authy_admin.admin import AuthyAdminUserAdmin
from authy_admin.forms import AuthyAuthenticationForm
from authy_admin.models import AuthyAdminUser

class AuthyAdminSite(AdminSite):
    
    """
    An AuthyAdminSite extends the default django AdminSite to provide
    staff members with a two-factor authentication scheme and 
    the configuration thereof powered by authy.com's REST API.

    """

    login_template = 'authy_admin/login.html'
    login_form = AuthyAuthenticationForm
    VERIFIED_FLAG_NAME = 'is_authy_verified'
    
    def __init__(self, name='admin', app_name='admin'):
        super(AuthyAdminSite, self).__init__(name, app_name)
        self.register(AuthyAdminUser, AuthyAdminUserAdmin)

    def has_permission(self, request):

        """
        override default has_permission to ensure user has authenticated
        via authy if configured to require it

        """

        has_perm = super(AuthyAdminSite, self).has_permission(request)

        if has_perm and self.require_authy_verification(request):
            if not self.has_authy_verification(request):
                logout(request)
                return False
        return has_perm

    @never_cache
    def login(self, request, extra_context=None):
        
        """
        override login to add flag to session that indicates the user
        logged in via the two-factor authentication scheme

        """

        response = super(AuthyAdminSite, self).login(request, extra_context)
        if super(AuthyAdminSite, self).has_permission(request):
            request.session[self.VERIFIED_FLAG_NAME] = True
        return response

    def require_authy_verification(self, request):

        """
        return True iff user is configured to require an authy
        two-factor authentication code when logging in

        """

        return AuthyAdminUser.objects.filter(user=request.user).exists()

    def has_authy_verification(self, request):
        
        """
        return True iff user has logged in via two-factor 
        authentication scheme
        
        """

        return request.session.get(self.VERIFIED_FLAG_NAME, False)
