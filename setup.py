from setuptools import setup
setup(
    name='fros',
    version='1.0',
    author="Jiri Moskovcak",
    author_email="jmoskovc@redhat.com",
    description=("Universal screencasting frontend with pluggable support "
                 "for various backends"),
    license = "GPLv2+",
    url = "https://github.com/mozeq/fros",
    scripts = ['src/fros'],
    packages=['pyfros', 'pyfros.plugins'],
    package_dir = {'pyfros': 'src/pyfros/', 'pyfros.plugins': 'src/pyfros/plugins'},
    data_files = [('share/man/man1',['fros.1'])]
)
