import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'oaGcLXwrx0XGec5RE33R2Q5gp3o7d6nkiZPcg80zSyCGuRVSFk'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://test:zaratustra@botmatrix.xyz/botmatrix'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = '6LceqHQUAAAAAHeq3tvyYhKpIjjQO2nV1eHk81z_'
    RECAPTCHA_PRIVATE_KEY = '6LceqHQUAAAAAMWBtGz3_TGuWSKc4j-5nYXT0QWf'
    RECAPTCHA_USE_SSL = True
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}