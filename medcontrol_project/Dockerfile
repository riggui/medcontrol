# Dockerfile pour Render
FROM python:3.12-slim

# Répertoire de travail
WORKDIR /app

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Exposer le port que Render utilisera
EXPOSE 10000

# Commande pour lancer Gunicorn avec ton projet Django
CMD ["gunicorn", "medcontrol_project.wsgi:application", "--bind", "0.0.0.0:10000"]
