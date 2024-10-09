import hashlib

def hash_func(data):
    concat_data = '1234'
    concant_hash = hashlib.sha256(concat_data.encode())
    data_hash = hashlib.sha256(data.encode())
    full_hash = data_hash.hexdigest() + concant_hash.hexdigest()

    return full_hash


recieved_hash = hash_func('bilal')
print(recieved_hash)
recieved_hash = hash_func('ahmed')
print(recieved_hash)
recieved_hash = hash_func('javed')
print(recieved_hash)
recieved_hash = hash_func('lauren')
print(recieved_hash)
recieved_hash = hash_func('hector')
print(recieved_hash)

