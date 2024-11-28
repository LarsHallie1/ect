from setuptools import setup, find_packages

setup(
    name='ect',
    description="environment comparison tool",
    author="Lars Hallie",
    author_email="lars.hallie@coolblue.nl",
    version='2.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'numpy',
        'toml',
    ],
    entry_points={
        'console_scripts': [
            'ect = ect.main:cli',
        ],
    },
)
