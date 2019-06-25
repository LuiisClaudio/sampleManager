"""call this module to setup your python packages via pip"""

from pip._internal import main as pip

pip_install_argument = "install"

# packages to install
packages_to_install = [
        "pygame",        #
        "scipy",        # 
        ]

def install(packages):
    """installes given packages via pip

    Args:
        package names as list

    Returns:
        None

    """
    global pip_install_argument
    for package in packages:
        pip([pip_install_argument, package])

if __name__ == '__main__':
    install(packages_to_install)