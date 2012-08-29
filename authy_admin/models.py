from authy.api import AuthyApiClient
from django.db import models
from django.conf import settings
from django.contrib.admin.models import User

class AuthyAdminUser(models.Model):

    """
    AuthyAdminUser instances enable two-factor authentication
    for the given user when authenticating with an AuthyAdminSite
    
    """

    user = models.OneToOneField(User, primary_key=True)
    authy_id = models.IntegerField(blank=True)
    country_code = models.IntegerField(default=1)
    phone_number = models.CharField(max_length=128)

    def save(self, *args, **kwargs):

        """
        override save to register user with authy.com and to save
        the third party user id for subsequent validation API calls

        """

        if not self.authy_id:
            authy_api = AuthyApiClient(settings.AUTHY_API_KEY)
            authy_user = authy_api.users.create(self.user.email,
                                                self.phone_number,
                                                self.country_code)
            if authy_user.ok():
                self.authy_id = authy_user.id

        super(AuthyAdminUser, self).save(*args, **kwargs)

    def check_token(self, token):

        """
        returns True iff token is a valid authy.com two-factor token
        for the given user

        """

        authy_api = AuthyApiClient(settings.AUTHY_API_KEY)
        verification = authy_api.tokens.verify(self.authy_id, token)
        return verification.ok()
