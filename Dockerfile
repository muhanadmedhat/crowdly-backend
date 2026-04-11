# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install dependencies
COPY req.txt .
RUN pip install --upgrade pip && pip install -r req.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the app using gunicorn
CMD ["gunicorn", "crowdlyBackend.wsgi:application", "--bind", "0.0.0.0:8000"]