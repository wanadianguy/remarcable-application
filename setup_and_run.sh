#!/bin/bash
echo "--- Setting up Django API ---"

# Create virtual environment if it doesn't exist
if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

echo "Starting Django development server"
python manage.py runserver localhost:8000
