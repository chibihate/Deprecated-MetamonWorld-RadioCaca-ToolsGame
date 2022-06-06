# Tools for Metamon World - Radio Caca
==================

[Metamon World]

[Metamon World]: https://metamon.radiocaca.com/

## Important disclaimer
This software is intended for use by individuals 
familiar with Python programming language. It uses
sensitive signature code from MetaMask wallet which 
needs to be safe and secure at all times. Make sure 
to inspect the code for any attempts to send your 
information anywhere except https://metamon-api.radiocaca.com/usm-api 
(official metamon game api). We are not responsible 
for any loss incurred if you used modified version 
of this code from other sources!

## Prerequisites

To start using this program Python needs to be 
installed and some packages. The easiest way to 
obtain Python is to install [miniconda], use 
latest release for your platform Linux/Mac/Windows

[miniconda]: https://docs.conda.io/en/latest/miniconda.html

After installation open command line with 
virtual environment activated and run following
command
    
    pip install requests prettytable python-dotenv

## Prepare wallet(s) information

Please reference <a href='https://github.com/MetaMon-game-player/MetamonPlayer'>this article</a> to get ADDRESS_WALLET, SIGN_WALLET, MSG_WALLET.

If you install successfully the library <a href='https://pypi.org/project/python-dotenv/'>python-dotenv</a>
- Change .env file and use desktop.py as a main file.
If not
- Change inside mobile.py and use it as a main file.

# Preparation is complete! 
## Ready to roll?

For <b>Desktop version</b>:

    python3 desktop.py
    

For <b>Mobile version</b>:

    python3 mobile.py
    
   
