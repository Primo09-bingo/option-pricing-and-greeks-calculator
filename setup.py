from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="options-calculator",
    version="1.0.0",
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="Un calculateur d'options Black-Scholes avec analyse des grecques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-utilisateur/option-pricing-calculator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'streamlit>=1.32.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'plotly>=5.13.0',
        'scipy>=1.10.0',
    ],
    entry_points={
        'console_scripts': [
            'options-calculator=options_calculator:main',
        ],
    },
)
