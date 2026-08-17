# daniel

[![Docker Hub Publish](https://github.com/molmodise026j-sketch/daniel/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/molmodise026j-sketch/daniel/actions/workflows/docker-publish.yml)

My first Python project where I'm learning the basics of Python 3.12.

## About

A Python project for learning the basics of Python 3.12. Still figuring out what to build!

This will serve as a sandbox for exploring:
- Basic syntax and data types
- Functions and control flow
- Object-oriented programming concepts
- File handling and modules

## Setup

Activate the virtual environment:

```bash
source vebv/bin/activate
```

## Docker

Build the Docker image locally:

```bash
docker build -t daniel:latest .
```

Run the container interactively (it will run `main.py`):

```bash
docker run --rm -it daniel:latest
```

To change the default command, override it with `docker run`:

```bash
# run the calculator instead
docker run --rm -it daniel:latest python calculator.py
```

## Publish to Docker Hub

Automated publish (GitHub Actions):

1. Create a repository named `daniel` (or any name) on Docker Hub.
2. In your GitHub repo settings, add two repository secrets:
	- `DOCKERHUB_USERNAME` — your Docker Hub username
	- `DOCKERHUB_TOKEN` — a Docker Hub access token (or your password)
3. Push to the `main` branch — the workflow at `.github/workflows/docker-publish.yml` will build and push the image as `DOCKERHUB_USERNAME/daniel:latest`.

Manual publish (local):

```bash
# login to Docker Hub
docker login --username YOUR_DOCKERHUB_USERNAME

# tag the locally-built image
docker tag daniel:latest YOUR_DOCKERHUB_USERNAME/daniel:latest

# push to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/daniel:latest
```

