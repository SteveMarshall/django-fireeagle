# django-fireeagle

**This library is deprecated, as Fire Eagle no longer exists**

The `django_fireeagle` package contains code to handle the Fire Eagle authorisation process within Django. You can use it to manage connections between Django users and their respective Fire Eagle access tokens.

To install, check the code out using this and place django_fireeagle somewhere on your Python path.

## Overview

The Django Fire Eagle package consists of:

*   Views to handle instigation and completion of Fire Eagle authorisation.
*   A database model to persist Fire Eagle access tokens.

## Dependencies

`django_fireeagle` uses the Python [OAuth](http://oauth.googlecode.com/svn/code/python/oauth/) and [fireeagle_api](http://github.com/SteveMarshall/fire-eagle-python-binding/) libraries, which must be installed somewhere on the Python path.

The package also depends on the availability of Django&#8217;s [session support](http://www.djangoproject.com/documentation/sessions/).

## Installation

Having ensured the `oauth`, `fireeagle_api`, and `django_fireeagle` packages are available on your Python path, you can add Fire Eagle interaction to your application by doing the following:

1.  Put `django_fireeagle` in your `INSTALLED_APPS` setting.
2.  Run the command `manage.py syncdb` to create the necessary tables.
3.  Add the following views to your urlconf:
    ```python
    ( r'fire-eagle/$', 'django_fireeagle.views.begin' ),
    ( r'fire-eagle/finalise/$', 'django_fireeagle.views.finalise' ),
    ```
4.  Set the callback URL in Fire Eagle to point to `yoursite.com/fire-eagle/finalise/`.

You will then be able to browse to `yoursite.com/fire-eagle/` to associate your logged-in Django user to a Fire Eagle account

## Accessing Fire Eagle

To interact with Fire Eagle on behalf of the current user:

```python
// Retrieve the current user's Fire Eagle OAuth token
fe_user = FireEagleUser.objects.get( user=request.user )
request_token = fe_user.get_fire_eagle_token()

// Instantiate a Fire Eagle instance using our app's token
fe = FireEagle(
    getattr( settings, 'FIREEAGLE_CONSUMER_KEY' ),
    getattr( settings, 'FIREEAGLE_CONSUMER_SECRET' )
)

// Make calls to the Fire Eagle API!
fe_user = fe.user( request_token )
```

## Example project

To use the included example:

1.  Create a test application on Fire Eagle, with the callback URL pointing to `http://127.0.0.1:8000/fire-eagle/finalise/`.
2.  Fill the `FIREEAGLE_CONSUMER_KEY` and `FIREEAGLE_CONSUMER_SECRET` in `settings.py` with the values for your Fire Eagle application.
3.  Run `python manage.py syncdb` in the project’s directory, and create a user.
4.  Run `python manage.py runserver` to start the app.
5.  Navigate to `http://127.0.0.1:8000/`, and follow the steps.
