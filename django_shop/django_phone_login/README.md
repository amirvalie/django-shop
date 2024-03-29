# Django Phone Login

Django Phone Login with both SMS verification and password

## Description

With this package, you can login or register with a password or SMS code verification to verify the user account. This package also has other features such as forgetting the password and changing the password.


### Dependencies

* Django

### Installing

* git clone https://github.com/amirvalie/django_phone_login.git

### Executing program

* Configuration settings.py 
```
INSTALLED_APPS += [
    ... 

    'django_phone_login'
]

AUTHENTICATION_BACKENDS = [
    'django_phone_login.backend.phone_backend.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend'
]

MIDDLEWARE = [
    ...

    'django_phone_login.middleware.IpAddressMiddleware',

]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

AUTH_USER_MODEL = 'django_phone_login.User'
```

* Add these fields to the settings to control the restrictions

```
EXPIRE_CACHE=20
DURATION_OF_OTP_VALIDATY=2
PHONE_LOGIN_ATTEMPTS=10
```

* Add the below urls.py

```
urlpatterns = [
    path('user/', include('django_phone_login.urls'),name='phone_login'),
]
```


## Authors

Contributors names and contact info

Amirhossein Valie
hosseinvalie@gmail.com 
