from setuptools import setup, find_packages


setup(
    name='sch_doc_parser',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'extract_components_to_csv=main.__main__:main'
        ]
    },
    install_requires=[
        'olefile==0.46'
    ],
)
