#!/bin/sh

# Wait for MySQL
echo "Waiting for MySQL..."
while ! nc -z db 3306; do
  sleep 0.1
done
echo "MySQL started"

# Initialize the database
python predeploy.init_db.py

# Start the main process
exec python app.py