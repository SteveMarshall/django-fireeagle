import urllib
import oauth

from django.contrib.auth.models import User
from django.db import models

class FireEagleUser( models.Model ):
    """Extension to User model to bind Fire Eagle credentials."""
    user = models.OneToOneField( User, raw_id_admin=True )
    fire_eagle_token  = models.CharField( editable=False, db_index=True, max_length=100 )
    fire_eagle_secret = models.CharField( editable=False, max_length=100 )
    
    def get_fire_eagle_token( self ):
        """Build an OAuthToken for Fire Eagle use"""
        token_string = urllib.urlencode({'oauth_token': self.fire_eagle_token, 'oauth_token_secret': self.fire_eagle_secret})
        return oauth.OAuthToken.from_string( token_string )
    
    def set_fire_eagle_token( self, token ):
        self.fire_eagle_token  = token.key
        self.fire_eagle_secret = token.secret
    
    def __str__(self):
        return "<User %s has Fire Eagle token %s>" % \
            (self.user, self.fire_eagle_token)
    
    class Admin:
        pass
    
