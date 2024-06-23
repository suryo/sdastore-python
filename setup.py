from distutils.core import setup
import py2exe

setup(
    windows=['sdastore.py'],  # Ganti 'main_script.py' dengan nama skrip utama Anda
    options={
        'py2exe': {
            'includes': [],
            'excludes': [],
            'dll_excludes': [],
            'bundle_files': 1,  # Bundle semua ke satu file (opsional)
            'compressed': True,
        }
    },
    zipfile=None,  # Jangan membuat file zip terpisah
)
