@echo off
echo --- Setting up Django API ---

REM Create virtual environment if it doesn't exist
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Apply migrations
echo Applying migrations...
python manage.py migrate

REM Start Django development server
echo Starting Django development server at http://127.0.0.1:8000/
python manage.py runserver
