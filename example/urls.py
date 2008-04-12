from django.conf.urls.defaults import *

urlpatterns = patterns( '',
    # Include admin simply for login/user creation
    ( r'^$', 'example.web.views.index' ),
    ( r'^admin/', include( 'django.contrib.admin.urls' ) ),
    
    ( r'^login/$', 'django.contrib.auth.views.login' ),
    
    # Fire Eagle auth
    ( r'fire-eagle/$', 'django_fireeagle.views.begin' ),
    ( r'fire-eagle/finalise/$', 'django_fireeagle.views.finalise' ),
)
