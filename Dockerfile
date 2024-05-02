# Use the official Python base image
FROM python:3.11.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# Create and set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project files to the container
COPY . /app/

# Expose the port on which the Django app will run
EXPOSE 8000

# Command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
