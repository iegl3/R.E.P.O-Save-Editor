import json
from lib.decrypt import decrypt_es3
from lib.encrypt import encrypt_es3

def read_file(file_path):
    """
    Decrypts the given file and returns its content as a UTF-8 string.
    """
    decrypted_data = decrypt_es3(file_path, "Why would you want to cheat?... :o It's no fun. :') :'D")
    return decrypted_data.decode('utf-8')

def save_as_json(file_path, data):
    """
    Saves the given data as a JSON file at the specified file path.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

input_file = "test_save_file.es3"

print("Reading file...")
file_content = read_file(input_file)
print(file_content)

print("Saving as JSON...")
save_as_json("output.json", json.loads(file_content))