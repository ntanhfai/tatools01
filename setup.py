from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tatools01",  # tên của gói thư viện
    version="3.0.7", 
    description="Thư viện hữu ích của Tuấn Anh.",
    url="https://pypi.org/project/tatools01/",
    author="Tuấn Anh - Foxconn",
    author_email="nt.anh.fai@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "ruamel.yaml", 
        "python-docx", "markdown", "beautifulsoup4",
    ],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"tatools01": [ "Thoi_gian/*", "md_word/*", ]},
    # package_dir={"": "ntanh"},
    # packages=find_packages(where="ntanh"),
    Homepage="https://github.com/ntanhfai/tact",
    Issues="https://github.com/ntanhfai/tact/issues",
    entry_points={
        "console_scripts": [
            "tact=tatools01.cli:console_main",
            "md2w=tatools01.cli_md2w:main",
        ],
    },

)
