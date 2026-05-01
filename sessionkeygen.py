import secrets

file = open("./.env", "at")

file.write("\nSESSION_KEY=" + secrets.token_hex(64))