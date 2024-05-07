"""Add some specifications for installation."""

from setuptools import setup, find_packages

setup(
    name="pomodoro_tracker",  # Nom de votre module
    version="0.1",  # Version de votre module
    packages=find_packages(),  # Trouve automatiquement les packages à inclure
    install_requires=[  # Liste des dépendances requises pour votre module
        "numpy",
        "matplotlib",
    ],
    entry_points={  # Définit les points d'entrée pour les scripts exécutables
        "console_scripts": [
            "pomodoro=pomodoro_tracker.pomodoro_logger:main",
            "pomodoro=pomodoro_tracker.plot_pomodoro_global:main",
        ],
    },
    author="Florian MAILLARD",  # Votre nom ou le nom de votre équipe
    author_email="florian.maillard@mailoo.org",  # Votre adresse e-mail
    description="Help to track and journaling pomodoro activity",  # Description de votre module
    long_description=open("README.md").read(),  # Description détaillée
    long_description_content_type="text/markdown",  # Le type de contenu du fichier README
    url="https://github.com/fmaillar/pomodoro_tracker",  # Lien vers votre projet ou votre page GitHub
    classifiers=[  # Liste de classifications pour votre module
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Version minimale de Python requise pour votre module
)
