from distutils.core import setup

setup(
    name = 'pyraid',
    version = '0.1.0',
    packages = ['pyraid'],
    package_dir = {'pyraid': 'src/pyraid'},
    scripts = ['scripts/pyraid-mount', 'scripts/pyraid-dump'],
    author = 'Cody Soyland',
    author_email = 'codysoyland@gmail.com'
)
