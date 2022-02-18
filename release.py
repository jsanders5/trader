from subprocess import call
from version import __version__
import tarfile
import os.path
import markdown
import shutil

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

def bundle():
    try:
        os.mkdir('dist\crypt')
    except FileExistsError:
        pass

    make_tarfile('Trader_v{}.tar.gz'.format(__version__),  'dist')

def convert_readme():
    with open('README.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text,extensions=['fenced_code', 'codehilite'])

    with open('dist\README.html', 'w') as f:
        f.write(html)

create_exes()
convert_readme()
bundle()