# Health-Ease

## Steps to run the project in new system

- Git clone the project from
- Create a virtual environment into the main directory of the project
  - Use command - "python -m venv env" 
  - Activate virtual environment using command 
    - for windows "env/bin/activate"
    - for ios "source env/bin/activate"
    - Here env is the name of the virtual environment
- Now install all the project dependencies 
  - use command - "pip install -r requirements.txt"
- Now configure the IDE to use the interpreter present inside the virtual environment
  - Steps for VSCode : -
   
    1. Open IDE
    2. Use shortcut ctrl+shift+p to open the command palette on windows (for mac try using cmd+shift+p)
    3. Type "Python Interpretor" and select custom path
       1. Navigate to HealthEase/env/Scripts and select file with name "python"
    
- Now generate the secret key 
  - To generate the secret key try following option
    1. Open python shell in your terminal or cmd prompt and type follwing two lines
      - from django.core.management.utils import get_random_secret_key
      - get_random_secret_key()
  - After generating the key, copy it and store it in ".env" file in the SECRET_KEY variable and restart django server
- Now you can run the project using cmd "python manage.py runserver"
