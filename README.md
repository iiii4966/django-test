# Django project

__This is the personal CRUD api project using python web framework django.__

### Built With

* [Django](https://www.djangoproject.com/)

### Prerequisites

* Python 3.8.6 or higher
    ```sh
    python --version
    ```
* poetry install  
    - If you want to use the poetry tool, install it from the link below.  
    ```sh
    https://python-poetry.org/docs/
    ```
    - after install, set the below on the .bashrc or .zshrc and so on  
    ```sh
    plugins=(
        ...
        poetry
    )
  
    export PATH="$HOME/.poetry/bin:$PATH"
    ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/iiii4966/django-test.git
   ```
2. Install packages  
   if poetry installed  
   ```shell script
   poetry install
   ```
   If there is an error below while installing the dependencies,
   ```shell script
   The current project's Python requirement (2.7.17) is not compatible
   with some of the required packages Python requirement:
   ...
   ```
   Change the poetry file header in the poetry installation path
   ```shell script
   ~/.poetry/bin/poetry
   ```
   ```shell script
   #!/usr/bin/env python -> #!/usr/bin/env python3 
   ```

<!-- USAGE EXAMPLES -->
### Usage

__If you're using poetry as a virtualenv, execute the command below.__
```shell script
poetry shell
```

#### run migration
```shell script
make migrate
```

#### run server
```shell script
make run
```

#### run test
```shell script
make test
```

#### run docker
```shell script
# local
make docker-local

# prod
make docker-prod
```

## License

Distributed under the DSF License. See `LICENSE` for more information.

## TODO
- [ ] docker-compose with nginx, postgresql 