from distutils.core import setup

setup(
    name='d',
    version='0.0.1',
    author='Steve Losh',
    author_email='steve@stevelosh.com',
    packages=['d'],
    scripts=['bin/d'],
    url='http://sjl.bitbucket.org/d/',
    license='LICENSE.markdown',
    description="Documentation generation that won't make you tear your hair out.",
    long_description=open('README.markdown').read(),
    install_requires=[
        'Markdown',
        'pyquery',
        'pygments'
    ],
)
