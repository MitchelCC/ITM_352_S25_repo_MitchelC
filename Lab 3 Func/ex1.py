from cryptography.fernet import Fernnet
key = Fernet.generate_key()
fernet = Fernet(key)

user_input = input ("Enter a string to encrypt: ")

#encrypt the string
encoded_input = user_input.encode()
encrypted_data = fernet.encrypt(encoded_input)

#decrypt the string
decrpted_data = fernet.decrypt(encrypted_data)  
decoded_output = decrypted_data.decode()

print(f"\nOriginal string: {user_input}")
print(f"Encrypted bytes:  {encrypted_data}")
print(f"Decrypted string: {decoded_output}")