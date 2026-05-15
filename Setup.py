from setuptools import setup

setup(
    name="proshare",
    version="1.0.0",
    description="Share files instantly on your local network",
    py_modules=["share"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "proshare=share:main",
        ],
    },
)