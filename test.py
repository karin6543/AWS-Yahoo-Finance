def my_hash_func(key: str) -> int:
  # this returns "ascii" value of a character
  ascii_val = ord(key[0].lower()) 
  return ascii_val - 97

print(my_hash_func('zEbRas have white stripes'))