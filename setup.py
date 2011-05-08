import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.5.0'

INSTALL_REQUIRES = [
    'getpaid.core >= 0.9.0',
    'setuptools',
    'zope.interface',
    'zope.component',
    'zope.annotation',
    ]

setup(
    name='getpaid.brownpapertickets',
    version=version,
    license = 'ZPL2.1',
    description='GetPaid Brown Paper Tickets payment processor functionality',
    long_description = (
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
        ),
    classifiers=[
        'Framework :: Plone',
        'Framework :: Zope3',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries',
        ],
    keywords='',
    author='getpaid community',
    author_email='getpaid-dev@googlegroups.com',
    url='http://code.google.com/p/getpaid',
    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['getpaid'],
    include_package_data=True,
    install_requires = INSTALL_REQUIRES,
    zip_safe = False,
    )
