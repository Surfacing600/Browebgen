import os

my_email = os.environ.get('MY_EMAIL')
my_email_password = os.environ.get('MY_EMAIL_PASSWORD')
sqlalchemy_database_uri = os.environ.get('DATABASE_URL')

print(my_email)
print(my_email_password)
print(sqlalchemy_database_uri)