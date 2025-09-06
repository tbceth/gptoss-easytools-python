from setuptools import setup, find_packages

setup(
    name="gpt-oss",
    version="0.1.0",
    description="Modular, extensible OpenAI-compatible tool calling service for local and remote LLMs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/gpt-oss",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai",
        "python-dotenv"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
