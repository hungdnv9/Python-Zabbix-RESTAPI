# python3
import hashlib
import sys

def generate_token(zb_username, zb_password):
	combine = hostname + password
	token = hashlib.md5(combine.encode('utf-8')).hexdigest()
	return token


def vertify_token(token, accept_tokens):
    if token in accept_tokens:
        return True
    else:
        return False

