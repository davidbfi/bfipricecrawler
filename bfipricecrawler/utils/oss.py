from datetime import datetime
import oss2
from config import oss_config


auth = oss2.Auth(oss_config['accessKeyId'], oss_config['accessKeySecret'])
bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket_name'])
file_carmudi = 'FileCrawled/Carmudi/carmudi_{}'.format(int(datetime.now().strftime('%Y%m%d')))
file_mobil = 'FileCrawled/Mobil123/mobil123_{}'.format(int(datetime.now().strftime('%Y%m%d')))
file_olx = 'FileCrawled/olx/olx_{}'.format(int(datetime.now().strftime('%Y%m%d')))


def create_object(bucket, file):
    bucket.delete_object(file)
    bucket.put_object_from_file(file, file)
    return "Object {} created".format(file)


create_object(bucket=bucket, file=file_carmudi)
create_object(bucket=bucket, file=file_mobil)
create_object(bucket=bucket, file=file_olx)
