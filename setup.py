from setuptools import setup

setup(
    name='pairing',
    version='0.1',
    py_modules=['pairing'],
    long_description=("See https://github.com/perrygeo/pairing")
    author="Matthew Perry",
    author_email="perrygeo@gmail.com",
    description=("Encode pairs of integers as single integer values using the Cantor pairing algorithm"),
    license="BSD",
    keywords="encoding pairing cantor",
    url="https://github.com/perrygeo/pairing",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
