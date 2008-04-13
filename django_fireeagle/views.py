from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect

from fireeagle_api import FireEagle

from django_fireeagle.models import FireEagleUser

@login_required
def begin( request ):
    """Start the Fire Eagle authorisation process"""
    # Store next param to use after finalise()
    if 'next' in request.GET.keys():
        request.session['fireeagle_auth_next'] = request.GET['next']
    
    fe = FireEagle(
        getattr( settings, 'FIREEAGLE_CONSUMER_KEY' ),
        getattr( settings, 'FIREEAGLE_CONSUMER_SECRET' )
    )
    
    # Store the request token as a way of tracing back the 
    # auth request to this user.
    # We'll replace this with their real token in finalise()
    request_token = fe.request_token()
    try:
        fe_user   = FireEagleUser.objects.get( user=request.user )
    except ObjectDoesNotExist:
        fe_user   = FireEagleUser( user=request.user )
    fe_user.set_fire_eagle_token( request_token )
    fe_user.save()
    
    # Send them off to FE to authorize us
    auth_url = fe.authorize( request_token )
    return HttpResponseRedirect( auth_url )

@login_required
def finalise( request, next_url='/' ):
    """Finalise the Fire Eagle authorisation process"""
    fe = FireEagle(
        getattr( settings, 'FIREEAGLE_CONSUMER_KEY' ),
        getattr( settings, 'FIREEAGLE_CONSUMER_SECRET' )
    )
    
    if 'fireeagle_auth_next' in request.session.keys():
        next_url = request.session['fireeagle_auth_next']
        del request.session['fireeagle_auth_next']
    
    # TODO: Raise exception when we don't get an oauth_token in the request
    
    # Get the user and update their token accordingly
    fe_user = FireEagleUser.objects.get(
        user=request.user,
        fire_eagle_token=request.GET['oauth_token']
    )
    user_access_token = fe.access_token( fe_user.get_fire_eagle_token() )
    fe_user.set_fire_eagle_token( user_access_token )
    fe_user.save()
    
    return HttpResponseRedirect( next_url )
