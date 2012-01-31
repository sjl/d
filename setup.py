from distutils.core import setup

setup(
    name='d',
    version='0.1.1',
    author='Steve Losh',
    author_email='steve@stevelosh.com',
    packages=['d'],
    scripts=['bin/d'],
    url='http://sjl.bitbucket.org/d/',
    license='MIT',
    description="Documentation generation that won't make you tear your hair out.",
    long_description='Read the documentation at http://sjl.bitbucket.org/d/',
    install_requires=[
        'Markdown',
        'pyquery',
        'pygments'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    package_data={'d': ['resources/*']},
)
