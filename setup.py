from setuptools import setup, find_packages

setup(
    name='Azure Cost Optimizer',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/upendrajangir/Azure-Cost-Optimizer.git',
    license='Apache 2.0',
    author='Upendra Jangir',
    author_email='upendrajangir9@gmail.com',
    description='A tool to optimize Azure cloud cost and manage subscriptions',
    install_requires=[
        'certifi',
        'charset-normalizer',
        'idna',
        'requests',
        'urllib3'
    ],
    classifiers=[
        'Development Status :: 0.1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License',
        'Programming Language :: Python :: 3.10',
    ],
    zip_safe=False
)
