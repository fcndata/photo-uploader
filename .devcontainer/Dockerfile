# Dockerfile para el contenedor de desarrollo de Python
FROM python:3.11

# Instalar dependencias del sistema necesarias para el proyecto
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Crear el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

CMD ["bash"]