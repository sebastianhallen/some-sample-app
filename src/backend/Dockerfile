FROM python:3.9

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN chown -R nobody:nogroup /app

USER nobody
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "1337"]
