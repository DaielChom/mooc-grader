def email_to_seed(email):
  seed = ""
  for i in email:
    seed = seed + str(ord(i))
  return int(seed)