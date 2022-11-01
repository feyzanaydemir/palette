from setuptools import setup

setup(
    name="palette",
    version="0.1.0",
    description="Python package for extracting colors from images.",
    url="https://github.com/feyzanaydemir/palette",
    license="MIT",
    python_requires=">=3.6",
    packages=["palette"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    entry_points={
        "console_scripts": ["palette=palette.command:main"],
    },
)
