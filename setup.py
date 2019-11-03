
import setuptools

setuptools.setup(
    name = "LabTools",
    author  =  "Luca Arnaboldi",
    author_email = "luca.arnaboldi@arn4.it",
    description = "Package with useful tool for Physics Laborayory Courses",
    url = "https://github.com/arn4/LabTools",
    packages = setuptools.find_packages(),
    python_requires = '>=3.6',
    install_requires = [
        'numpy',
        'uncertainties',
        'matplotlib',
        'tikzplotlib',
        'scipy',
        'pyaml'
    ]
)
