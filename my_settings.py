DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'idus',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}

SECRET_KEY = {
    'secret' : 'as#9%kh!=uux9f5n3lx9!e4@n17$+)lo9i3r#&rr2cfhkz0fn-',
    'algorithm' : 'HS256' 
}
