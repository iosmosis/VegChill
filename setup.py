from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import ConfigParser
import os

APP_NAME = 'VegChill'
APP_AUTHOR = 'Anciety'

INSTALL_SCRIPT = r'''
import lldb
import os
import vegchill

def __lldb_init_module(debugger, internal_dict):
    vegchill.lldb_init_module(debugger, internal_dict, {})
'''

def post_install_init(app_path, rewrite_config=True, develop=False):
    app_config_path = os.path.join(app_path, 'config')
    app_install_script_path = os.path.join(app_path, 'load_vegchill.py')
    if rewrite_config or not os.path.exists(app_config_path):
        config = ConfigParser.ConfigParser()
        config.add_section('plugin')
        config.add_section('option')
        if develop:
            config.set('option', 'verbose', 'true')
        else:
            config.set('option', 'verbose', 'false')
        with open(app_config_path, 'w') as f:
            config.write(f)
    
    # write load script
    with open(app_install_script_path, 'w') as f:
        if develop:
            f.write(INSTALL_SCRIPT.format("config_path='develop_app/config'"))
        else:
            f.write(INSTALL_SCRIPT.format(''))


class PostDevelopCommand(develop):
    def run(self):
        develop_app_dir = 'develop_app'
        if not os.path.exists(develop_app_dir):
            os.mkdir(develop_app_dir)
        post_install_init(develop_app_dir, develop=True)
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        import appdirs
        app_path = user_data_dir(APP_NAME, APP_AUTHOR)
        if not os.path.exists(app_path):
            os.mkdir(app_path)
        post_install_init(app_path)
        install.run(self)

setup(
    name=APP_NAME,
    version='0.1.0',
    packages=find_packages('src'),
    install_requires=[
        'appdirs >= 1.4.3',
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    author=APP_AUTHOR,
    author_email='ding641880047@126.com',
    description='Veg Chickens lldb enhencement plugin',
    keywords='lldb plugin',
)