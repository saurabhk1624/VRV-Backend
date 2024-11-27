# Project Name

A brief description of your project. Highlight its purpose and functionality.

## Prerequisites

Before getting started, make sure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the Repository

```bash
git clone git@github.com:saurabhk1624/VRV-Backend.git

```


### 2. Create the `secret.py` File

i). In the root of the project directory, create a file named `secret.py`.
ii). Add the following content to the file, replacing the placeholders with your actual database credentials:

   ```python
   # secret.py
   DB_NAME = "your_database_name"
   DB_USER = "your_database_user"
   DB_PASSWORD = "your_database_password"
```

### 3. Starting the container

To start container do the following:
```bash
i). cd VRV-Backend/docker/non-production
ii). docker compose build
iii). docker compose up -d
```





