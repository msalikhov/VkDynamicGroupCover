import glob
import os

from Package.Config import *
from Package.UploadedPhoto import UploadedPhoto
from Package.Utils import print_data, sleep
from Package.VkApi import get_group_cover_photo_upload_server, upload_photo, save_photo


def get_photo_files(path):
    paths = glob.glob(path + '/*')
    photos = []
    for photo_path in paths:
        photos.append({'photo': open(photo_path, 'rb')})
    return photos


def upload_photos(photo_files):
    uploaded_photos = []
    for photo_file in photo_files:
        photo_upload_url = get_group_cover_photo_upload_server(group_id, group_access_token)
        photo_hash, photo_code = upload_photo(photo_upload_url, photo_file)

        uploaded_photos.append(UploadedPhoto(photo_upload_url,
                                             photo_hash,
                                             photo_code,
                                             group_access_token))
    return uploaded_photos


def switch_photos():
    photos_dir_path = os.path.join(os.path.dirname(__file__), photos_dir_name)
    photo_files = get_photo_files(photos_dir_path)
    uploaded_photos = upload_photos(photo_files)

    while len(uploaded_photos) > 0:
        for uploaded_photo in uploaded_photos:
            try:
                save_photo(uploaded_photo)
                sleep(repeat_interval)
            except Exception as e:
                print_data(e, '\n')
                sleep(error_interval)


switch_photos()
