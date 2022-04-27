from subprocess import call
from version import __version__
import tarfile
import os.path
import markdown
import shutil
import boto
import boto.s3
import sys
from boto.s3.key import Key

def make_tarfile(output_filename, source_dir):
    os.chdir('dist')
    with tarfile.open(output_filename, "w:gz") as tar:
        for name in os.listdir("."):
            tar.add(name)
        tar.close()
#         tar.add(source_dir, arcname=os.path.basename(source_dir))

def create_exes():
    call("pyinstaller --onefile trader.py".format(__version__))
    call("pyinstaller --onefile generate_encrypted_api_keys.py".format(__version__))

def bundle(base_filename):
    try:
        os.mkdir('dist\crypt')
    except FileExistsError:
        pass

    make_tarfile(base_filename + '.tar.gz',  'dist')
    return base_filename + '.tar.gz'

def convert_readme():
    with open('README.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text,extensions=['fenced_code', 'codehilite'])

    with open('dist\README.html', 'w') as f:
        f.write(html)

def upload(filename):
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

    bucket_name = 'trader-files-s3'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)


#     bucket = s3_connection.get_bucket(bucket_name)

    print('Uploading {} to Amazon S3 bucket {}'.format(filename, bucket_name))

    bucket = conn.get_bucket(bucket_name)

    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    k = Key(bucket)
    k.key = os.path.basename(filename)
    k.set_contents_from_filename(filename,
        cb=percent_cb, num_cb=10)

create_exes()
convert_readme()
filename = bundle('Trader_v{}'.format(__version__))
# upload('dist\\'+filename)
#
# upload('dist\\README.html')