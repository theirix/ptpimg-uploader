from setuptools import setup

with open('README.rst') as desc:
    long_description = desc.read()

setup(
    name="ptpimg_uploader",
    version="0.9",
    author="theirix",
    author_email="theirix@gmail.com",
    description=(
        "PTPImg uploader, handles local files and URLs, from the commandline"),
    long_description=long_description,
    license="BSD",
    keywords="image uploader",
    url="https://github.com/theirix/ptpimg-uploader",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
    ],
    py_modules=['ptpimg_uploader'],
    entry_points={
        'console_scripts': [
            'ptpimg_uploader = ptpimg_uploader:main',
        ],
    },
    install_requires=[
        'requests',
    ],
    python_requires=">=3.3"
)
