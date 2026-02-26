from setuptools import setup

NAME = 'SourceDetect'
DESCRIPTION = 'Build, train, and implement a CNN model for detecting real objects in TESS data'
URL = 'https://github.com/andrewmoore73/SourceDetect'
EMAIL = 'andrewnmoore73@gmail.com'
AUTHOR ='Andrew Moore'
VERSION = '1.0.0'
REQUIRED = ['keras>=3.0',
            'tensorflow>=2.16',
            'scikit-learn>=1.7',
            'numpy',
            'matplotlib',
            'photutils',
            'pandas'
            ]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author_email=EMAIL,
    author=AUTHOR,
    packages=['sourcedetect'],
    install_requires=REQUIRED,
    include_package_data=True
)

