FROM python:3.10

WORKDIR /app

<<<<<<< HEAD
=======
# Keys from OpenAI etc.
COPY .env .env

>>>>>>> c2b0f4d (Dockerizing with docker compose. And adding missing dependencies in requirements.txt)
# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

# Copy app code and set working directory
COPY . .

# Expose port you want your app on
EXPOSE 8501

# Run
ENTRYPOINT ["streamlit", "run", "src/main.py", "–server.port=8501", "–server.address=0.0.0.0"]