class UploadedPhoto:
    server = None
    hash = None
    code = None
    token = None

    def __init__(self, server, photo_hash, photo_code, token):
        self.server = server
        self.hash = photo_hash
        self.code = photo_code
        self.token = token
