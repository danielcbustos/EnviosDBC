# Usar la imagen base de Python 3.9
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requerimientos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido de la aplicación en el contenedor
COPY . .

# Exponer el puerto en el que corre la aplicación Flask
EXPOSE 3000

# Ejecutar las pruebas
RUN python -m unittest discover tests
RUN coverage run -m unittest discover tests
RUN coverage report

# Definir el comando para ejecutar la aplicación y las pruebas
#CMD sh -c "python -m unittest discover tests && python app.py"

# CMD ["python", "-m", "unittest", "discover", "tests"]
# Comando para iniciar la aplicación
CMD ["python", "app.py"]
