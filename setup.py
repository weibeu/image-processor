from setuptools import setup, find_packages


VERSION = "0.1"


requirements = [
    "requests",
    "flask",
    "flask_restful",
    "pillow",
    "gunicorn"
]


setup(
    name='Image-Processor',
    version=VERSION,
    url='https://github.com/thec0sm0s/image-processor',
    license='MIT',
    author='□ | The Cosmos',
    author_email='deepakrajko14@gmail.com',
    description='An image processing server.',
    platforms='any',
    install_requires=requirements,
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
