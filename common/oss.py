import logging

import oss2

import helper as _helper

_config = _helper.get_config()
_storage_config = _config['storage']
_oss_config = _storage_config['oss']

if _storage_config['use_oss']:
    endpoint = 'http://oss-cn-beijing.aliyuncs.com'
    auth = oss2.Auth(_oss_config['access_key_id'], _oss_config['access_key_secret'])
    bucket = oss2.Bucket(auth, endpoint, _oss_config['bucket_name'])


def upload_to_oss_storage(source_file_name, destination_blob_name):
    bucket.put_object_from_file(destination_blob_name, source_file_name)


def upload_oss_images(source_file_path, dest_file_name):
    upload_to_oss_storage(source_file_path, 'images/%s' % dest_file_name)
