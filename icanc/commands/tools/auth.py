import keyring

def set_auth(key, user, password):
    keyring.set_password(key, "user", user)
    keyring.set_password(key, "password", password)

def get_auth(key):
    return dict(
        user = keyring.get_password(key, "user"),
        password = keyring.get_password(key, "password"),
    )
