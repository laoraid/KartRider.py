from setuptools import find_packages, setup
from __about__ import __author__, __version__

setup(
    name='KartRider',
    version=__version__,
    url='https://github.com/laoraid/KartRider.py',
    license='MIT',
    author=__author__,
    author_email='a99azaz@gmail.com',
    description='KartRider Open API Python wrapper',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    keywords=['KartRider'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Korean',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['requests'],
    python_requires='>=3.6'
)
