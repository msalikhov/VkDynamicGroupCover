class Group:
    photos_subdir_name = None
    group_id = None
    group_token = None
    uploaded_photos = None

    def __init__(self, photos_subdir_name, group_id, group_token):
        self.photos_subdir_name = photos_subdir_name
        self.group_id = group_id
        self.group_token = group_token
