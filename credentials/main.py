import bcrypt
import time

password = "0f500c90-9df1-4bd4-b789-b89f1a1bcf65"

bytes_password = password.encode('utf-8')

# generate a timestamp-based salt
# salt_timestamp = str(int(time.time())).encode('utf-8')

# create timestamp in this format: YYYY-MM-DDTHH:MM:SS.mmmmmmmZ
foundationtimestamp = time.strftime("YYYY-MM-DDTHH:MM:SS.mmmmmmmZ", time.gmtime()).encode('utf-8')

# salt = bcrypt.gensalt()

hash = bcrypt.hashpw(bytes_password, foundationtimestamp)

print("Password:", password)
print("Timestamp:", foundationtimestamp)
# print("Salt:", salt.decode('utf-8'))
print("Hashed Password:", hash.decode('utf-8'))
