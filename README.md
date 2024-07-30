# Feedsphere

Feedsphere is a self-hosted web service designed for storing and managing RSS articles. Built using Falcon for its simplicity and a welcome break from the Spring framework's magic.

**Warning: This app is not production-ready; it is intended for experimental use with Falcon.**

 by chatgpt bro

## Getting Started

1. Run `setup.sh` to install the required dependencies. (Linux only)

    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

2. Run migrations using the following commands:

    ```bash
    PYTHONPATH={yourpath} alembic -c ./app/database/alembic.ini revision --autogenerate
    PYTHONPATH={yourpath} alembic -c ./app/database/alembic.ini upgrade head
    ```

3. Start the project:

    ```bash
    PYTHONPATH={yourpath} python3 app/main.py
    ```

4. To set up the application with a new admin and a changed `APP_KEY`, use:

    ```bash
    PYTHONPATH={yourpath} python3 app/main.py --setup
    ```

    This will create a new admin, and other users won't be able to sign in.


5. For development purposes, run the application with:

    ```bash
    PYTHONPATH={yourpath} python3 app/main.py --development
    ```
