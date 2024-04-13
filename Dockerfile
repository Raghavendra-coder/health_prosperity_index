# Use an official Python 3.9.6 runtime as a parent image
FROM python:3.9.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
COPY db.sqlite3 /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Uncomment the line below if you want to run a Streamlit app as the default command
#CMD ["streamlit", "run", "streamlit_file.py", "--server.port", "8502"8502]
