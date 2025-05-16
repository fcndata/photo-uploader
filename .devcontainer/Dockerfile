# Docker Python Image to load
FROM python:3.11

# Install OS-level dependencies (Linux) needed for the project
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies into the image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Start a bash shell for development
CMD ["bash"]

# Expose the port for the web server
EXPOSE 8000