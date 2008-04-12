from django.conf import settings
from django.shortcuts import render_to_response

from django_fireeagle.models import FireEagleUser
from fireeagle_api import FireEagle

def index( request ):
    """Offer a link to login, auth with Fire Eagle, or show Fire Eagle data"""
    if request.user.is_authenticated():
        
        fe_users = FireEagleUser.objects.filter( user=request.user )
        if 1 == len( fe_users ):
            # Yay, we're Fire Eagle ready, so get something to prove it
            request_token = fe_users[0].get_fire_eagle_token()

            fe = FireEagle(
                getattr( settings, 'FIREEAGLE_CONSUMER_KEY' ),
                getattr( settings, 'FIREEAGLE_CONSUMER_SECRET' )
            )

            fe_user = fe.user( request_token )
            
            return render_to_response( 'web/fire-eagle.html', {
                'user':    request.user,
                'fe_user': fe_user
            } )
        
        # Don't have Fire Eagle deets yet, so ask for them
        return render_to_response( 'web/logged-in.html', {
            'user': request.user 
        } )
    
    # Not logged in yet, so do that
    return render_to_response( 'web/logged-out.html' )
    