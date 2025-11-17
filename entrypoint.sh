#!/bin/sh
set -e

# Set the FLASK_APP environment variable for all subsequent commands
export FLASK_APP=src.app.app

# Define the path to the database file within the container
DB_PATH="/app/links.db"

# Check if the database file does not exist
if [ ! -f "$DB_PATH" ]; then
    echo "Database file not found at $DB_PATH. Initializing..."
    # Initialize the database using the flask command
    flask initdb
else
    echo "Database already exists. Skipping initialization."
fi

# Execute the main command passed to the script (the Dockerfile's CMD)
exec "$@"
