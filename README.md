# Get stuff running

Sample frontend and backend applications to be used to test out various ways of getting applications to run.

## Frontend

The frontend is just a static index.html that tries to fetch a tip from the backend and display it.

### Building and running

No actual build process needed -- edit index.html to point to an appropriate backend endpoint.

You can just open src/frontend/index.html directly in your browser or run it in a docker container with nginx:

```shell
cd src/frontend
docker build -t app-frontend .
docker run --rm -p 8080:80 app-frontend
```

If running in docker, open your browser and go to <http://localhost:8080>

## Backend

API for getting a tip of the day in the format:

```json
{
    "tipOfTheDay": "Some tip"
}
```

Tips can be sourced from various sources. API only has one route: `GET /` that serves the response.

### Building and running

You can build and run the backend in a docker container.

```shell
cd src/backend
docker build -t app-backend .
docker run --rm -p 1337:1337 app-backend
```

If you have python installed you can also run it directly.

```shell
cd src/backend
pip install -r requirements.txt
python serve.py
```

Once the backend is running, open your browser and go to <http://localhost:1337>.