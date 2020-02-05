from setuptools import setup

setup(
    name='d',
    version='0.2.2',
    python_requires='>=3',
    author='Steve Losh',
    author_email='steve@stevelosh.com',
    packages=['d'],
    scripts=['bin/d'],
    url='https://docs.stevelosh.com/d/',
    license='MIT',
    description="Documentation generation that won't make you tear your hair out.",
    long_description='Read the documentation at https://docs.stevelosh.com/d/',
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
