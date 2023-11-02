import os

db_user = os.environ.get('EMAIL_USER')

# db_pass = os.environ.get('DB_PASS')

db_pass = os.environ.get('EMAIL_PASS')
print(db_user)

print(db_pass)
