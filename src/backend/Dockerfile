FROM python:3.9

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN chown -R nobody:nogroup /app

USER nobody
ENTRYPOINT ["python"]
CMD ["/app/serve.py"]
