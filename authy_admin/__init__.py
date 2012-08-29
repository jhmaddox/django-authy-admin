from django.contrib import admin as default_admin
from authy_admin.sites import AuthyAdminSite

# replace django's default admin site with our version
default_admin.site = AuthyAdminSite()
