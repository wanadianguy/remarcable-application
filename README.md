# Catalog project

## Overview
This is a small project using Django to simulate a catalog API. The goal is to create a simple web application that allows users to search for products based on their description, category, and tags.

## Requirements

### To launch it locally
- Have Python 3.8 or higher installed.

### To launch it via Docker
- Have Docker installed.
- Run a Docker daemon.

## Launch project

### Locally
- Clone the project from the remote git repository.
- While at the root of this project, run either `./your_script.sh` or `my_script.bat`.
  *(On Linux/MacOS, some privileges might cause issues, so you may need to run `chmod +x your_script.sh` first.)*
- With a web browser, go to `http://localhost:8000`

### Via Docker
- Clone the project from the remote git repository.
- While at the root of this project, run `docker compose up -d`.
- With a web browser, go to `http://localhost:8000`

## Additional information
- The credentials for `http://localhost:8000/admin` are:
  **Username:** `admin`
  **Password:** `admin`

# To go further
Some further improvements could be made to this codebase. Here are a few I thought of during development:

- Enrich the API with more in-depth functionalities. Additional endpoints could be created to facilitate data handling and processing.
- Use an external database to separate the API and database, improving security and scalability.
- Improve the API's resiliency. Although most basic cases are covered, some more complex behaviors might still be missing.
- Complete or refactor the tests to cover all functionalities and ensure future changes won’t break anything.
- Add some pagination to the API endpoints to handle large datasets efficiently.
- Implement rate limiting to prevent abuse and ensure fair usage.
- Add some caching mechanisms to improve performance and reduce load on the database.
