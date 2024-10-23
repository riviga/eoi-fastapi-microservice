FROM python:3.12-slim
RUN pip install datetime
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY ./code /app
CMD ["python", "/app/main.py"]
