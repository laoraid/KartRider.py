from setuptools import find_packages, setup

setup(
    name='KartRider.py',
    version='0.1.0',
    url='https://github.com/laoraid/KartRider.py',
    license='MIT',
    author='Laoraid',
    author_email='a99azaz@gmail.com',
    description='KartRider Open API Python wrapper',
    packages=find_packages(exclude=['tests']),
    keywords=['KartRider'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Korean',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['requests', 'tqdm'],
    python_requires='>=3.6'
)
