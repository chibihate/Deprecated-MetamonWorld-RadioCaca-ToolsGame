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

Please reference <a href='https://github.com/MetaMon-game-player/MetamonPlayer'>this article</a> to get ADDRESS_WALLET, SIGN_WALLET, MSG_WALLET, ACCESS_TOKEN.

If you install successfully the library <a href='https://pypi.org/project/python-dotenv/'>python-dotenv</a>
- Change .env file and use <a href='https://github.com/chibihate/Metamon-RadioCaca-Tools#desktop-version'>desktop.py</a> as a main file.

If not
- Change inside <a href='https://github.com/chibihate/Metamon-RadioCaca-Tools#mobile-version'>mobile.py</a> and use it as a main file.

# Preparation is complete! 
## Desktop version:

    python3 desktop.py
    
If <b>ACCESS_TOKEN</b> is still valid, we go to dashboard.

If not, message will be like:

    Code is sending to your email. Kindly check
    Please fill your code:
    0000 (You put 2FA from your email)
    Email is verified

Dashboard message:
    
    1. Play game
    2. Market game
    0. Exit
    Please select you want to choose
    
Play game message:

    1. Battle in Island
    2. Mint eggs
    3. Show all metamons
    4. Up attribute all monsters   
    5. Join the best squad in Lost world
    6. Battle record in Lost world
    7. Get status my teams in Lost world
    0. Exit
    Please select you want to choose
    
Market game message:

    1. Check bag
    2. Shopping
    3. Shelling
    4. Canceling
    5. Buy item in drops
    6. Transaction history
    0. Exit
    Please select you want to choose

## Mobile version:

    python3 mobile.py
        
Message:

    Code is sending to your email. Kindly check
    Please fill your code:
    0000 (You put 2FA from your email)
    Email is verified
        
Dashboard message:
    
    1. Play game
    2. Market game
    0. Exit
    Please select you want to choose
    
Play game message:

    1. Battle in Island
    2. Mint eggs
    3. Up attribute all monsters   
    4. Join the best squad in Lost world
    5. Battle record in Lost world
    6. Get status my teams in Lost world
    0. Exit
    Please select you want to choose
    
Market game message:

    1. Check bag
    2. Shopping
    3. Shelling
    4. Canceling
    5. Buy item in drops
    6. Transaction history
    0. Exit
    Please select you want to choose

Hope you will have fun playing and this script will make it a little bit less tedious. Enjoy!
