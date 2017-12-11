# CSRF form protection
WTF_CSRF_ENABLED = False
# Database connection
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
# Secret key for encryption
SECRET_KEY = #import os; os.urandom(24)

# Email settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_PASSWORD = # -- 
MAIL_USERNAME = # --
