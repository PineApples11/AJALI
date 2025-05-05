# Use Python 3.8 image to match Pipfile
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy only Pipfile and Pipfile.lock first (for caching)
COPY Pipfile Pipfile.lock /app/

# Install dependencies using pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the app
COPY . /app

# Set environment variables
ENV FLASK_APP=Models/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["pipenv", "run", "flask", "run"]
