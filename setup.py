from setuptools import find_packages, setup

with open("README.md", encoding="UTF-8") as f:
    long_desc = f.read()

setup(
    name='1k-ursina-core',
    description='An easy to use extension module for Ursina.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    version='5.3.0',
    url='https://github.com/1k-Games/1k-core-ursina',
    author='1k Games',
    author_email='1k-games@proton.me',
    license='MIT',
    keywords='game development',
    packages=find_packages(),
    include_package_data=True,
    
    # TODO: Check Install
    install_requires=[
        'panda3d',
        'panda3d-gltf',
        'pillow',
        'pyperclip',
        'screeninfo',
        'ursina'
    ],

    # TODO: Check Extras
    extras_require={'extras': [
        'numpy',
        'imageio',
        'psd-tools3',
        'psutil',
        ],
    },
    python_requires='>=3.10',
)