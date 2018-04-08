from setuptools import setup

setup(
    name='ccxt-backtest',
    version='0.0.1',
    description='A wrapper for ccxt exchanges which provides backtesting functionality.',
    url='https://github.com/c4tz/ccxt-backtest',
    author='c4tz',
    packages=['backtest'],
    install_requires=[
        'ccxt==1.12.111',
        'python-dateutil==2.7.2'
    ]
)