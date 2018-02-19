import glob
import os
import threading
import configparser

from Package.Group import Group
from Package.UploadedPhoto import UploadedPhoto
from Package.Utils import print_data, sleep
from Package.VkApi import get_group_cover_photo_upload_server, upload_photo, save_photo

photos_dir_name = 'photos'
repeat_interval = 60
error_interval = repeat_interval * 10


def get_groups():
    groups = []
    config = configparser.ConfigParser()
    config.read("Config.ini")
    sections = config.sections()
    for section_name in sections:
        if section_name == 'Example':
            continue
        section = config[section_name]
        groups.append(Group(
            section['subdir_name'],
            section['id'],
            section['token']
        ))

    count = len(groups)
    print('%d groups read from config' % count)
    if count == 0:
        raise Exception("at least 1 group should be specified")
    else:
        for g in groups:
            print(g.photos_subdir_name, g.group_id, g.group_token)

    return groups


def get_photo_files(path):
    paths = glob.glob(path + '/*')
    photos = []
    for photo_path in paths:
        photos.append({'photo': open(photo_path, 'rb')})
    return photos


def upload_photos(photo_files, group):
    uploaded_photos = []
    for photo_file in photo_files:
        photo_upload_url = get_group_cover_photo_upload_server(group.group_id, group.group_token)
        photo_hash, photo_code = upload_photo(photo_upload_url, photo_file)

        uploaded_photos.append(UploadedPhoto(
            photo_upload_url,
            photo_hash,
            photo_code,
            group.group_token))
    return uploaded_photos


def prepare_group_photos():
    groups = get_groups()
    for group in groups:
        group_photos_subdir_path = os.path.join(
            os.path.dirname(__file__),
            photos_dir_name + "/" + group.photos_subdir_name)
        group_photo_files = get_photo_files(group_photos_subdir_path)
        group.uploaded_photos = upload_photos(group_photo_files, group)
    return groups


def switch_photos(group):
    uploaded_photos = group.uploaded_photos
    if len(uploaded_photos) == 0:
        print_data("no photos for group:", group.group_id)
        return
    while True:
        for uploaded_photo in uploaded_photos:
            try:
                save_photo(uploaded_photo)
                sleep(repeat_interval, group.group_id)
            except Exception as e:
                print_data(e)
                sleep(error_interval, group.group_id)


def proceed_in_background_thread(func, args):
    thread = threading.Thread(target=func, args=(args,))
    thread.daemon = True
    thread.start()


def start():
    groups = prepare_group_photos()
    first_group = groups.pop(0)
    for group in groups:
        proceed_in_background_thread(switch_photos, group)
    switch_photos(first_group)
    # execute switch for first group in foreground thread to block runtime


start()
