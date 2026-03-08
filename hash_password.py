import bcrypt

password = "Admin@Mubeen123"
hashed = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()
)
print("Your hashed password:")
print(hashed.decode('utf-8'))