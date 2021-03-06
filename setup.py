from setuptools import setup, find_packages

setup(
    name="deply",
    version='1.0',
    description='setup deply',
    long_description='',
    license='MIT',
    install_requires=['paramiko', 'PyYAML'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'deply=Deploy:main'
        ]
    },
)
