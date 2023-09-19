import os
import os.path

from setuptools import find_packages
from setuptools import setup


def find_requires():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    requirements = []
    with open('{0}/requirements.txt'.format(dir_path), 'r') as reqs:
        requirements = reqs.readlines()
    return requirements


if __name__ == '__main__':
    setup(
        name='SlurmDE',
        version='0.0.1',
        description='''Пакет выбирает данные с API http://5.159.103.105:4000/
            api/v1/logs и сохраняет на диск в файл customs_data.csv''',
        packages=find_packages(),
        install_requires=find_requires(),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'start_fetching = SlurmDE.cli:start',
            ],
        },
    )
