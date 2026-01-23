#!/usr/bin/env python3
"""
Setup script for Luxbin Quantum Internet Software Suite.
Installs the package for classical use and quantum integration.
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="luxbin-quantum-internet",
    version="1.0.0",
    description="Software suite for quantum networking with photonic and diamond quantum computer support",
    author="Luxbin",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'luxbin-translator=luxbin_translator:main',
            'quantum-internet=quantum_internet_service:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
)