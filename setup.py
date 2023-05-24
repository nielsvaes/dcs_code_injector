from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

data_files_to_include = ["*.png", "*.jpg"]

setup(
    name='dcs-code-injector',
    version='1.0.1',
    packages=find_packages(),
    package_data={
        "": data_files_to_include,
    },
    url='https://www.github.com/nielsvaes/dcs_code_injector',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ez-icons", "PySide6", "ez_qt", "ez_settings", "ez_utils", "qt_material"],
    license='GNU v3',
    author='Niels Vaes',
    author_email='nielsvaes@gmail.com',
    description='A REPL to use with Digital Combat Simulator to execute code while a mission is running.',

    entry_points = {
        'console_scripts': ['dcs-code-injector=dcs_code_injector.app:main'],
    },
)
