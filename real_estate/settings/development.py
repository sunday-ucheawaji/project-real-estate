from .base import *


DATABASES = {
    "default": {
        'ENGINE': env("POSTGRES_ENGINE"),
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': 'HOLYBOY',
        'HOST': env("PG_HOST"),
        'PORT': env("PG_PORT")
    }
}
