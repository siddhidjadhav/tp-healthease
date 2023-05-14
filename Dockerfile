# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app


# Copy the current directory contents into the container at /app


# COPY ./static /app/static
# COPY . .

# Install any needed packages specified in requirements.txt



# Set environment variable for Django
# ENV PYTHONUNBUFFERED=1
# ENV DJANGO_SETTINGS_MODULE=chico_healthcare.settings
# ENV STATIC_URL=/static/
# ENV STATIC_ROOT=/app/static/

# WORKDIR /app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./




# RUN python manage.py collectstatic --noinput

# Expose port 8080 to the outside world
EXPOSE 8080

# Run the command to start the server
CMD ["gunicorn", "chico_healthcare.wsgi:application", "--bind", "0.0.0.0:8080"]
