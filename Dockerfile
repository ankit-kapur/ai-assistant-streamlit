FROM python:3.10

WORKDIR /app

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