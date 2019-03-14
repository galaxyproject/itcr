# this script is used to boot a Docker container
source venv/bin/activate
exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - echo.app:app
