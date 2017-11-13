from Package.RequestsHelper import make_request, response, error, access_token

api_ver = '5.68'

host = 'https://api.vk.com/method/'
photos_api = host + 'photos.'


def make_intercepted(url, params, method, files=None):
    params['v'] = api_ver
    j = make_request(url, method, params, files).get_json()
    if response in j:
        return j[response]
    elif error in j:
        raise EnvironmentError(j[error])
    else:
        return j


def make_intercepted_get(url, params):
    return make_intercepted(url, params, 'get')


def make_intercepted_post(url, params, files=None):
    return make_intercepted(url, params, 'post', files)


def get_group_cover_photo_upload_server(group_id, group_token, crop_x1=None, crop_y1=None, crop_x2=1590, crop_y2=400):
    p = {'group_id': group_id, 'crop_x': crop_x1, 'crop_y': crop_y1, 'crop_x2': crop_x2, 'crop_y2': crop_y2,
         access_token: group_token}
    return make_intercepted_get(photos_api + 'getOwnerCoverPhotoUploadServer', p)['upload_url']


def upload_photo(upload_server_url, photo_file):
    r = make_intercepted_post(upload_server_url, {}, photo_file)
    return r['hash'], r['photo']


def save_photo(uploaded_photo):
    p = {'server': uploaded_photo.server, 'hash': uploaded_photo.hash, 'photo': uploaded_photo.code,
         access_token: uploaded_photo.token}
    return make_intercepted_get(photos_api + 'saveOwnerCoverPhoto', p)
