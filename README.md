# Django project

__This is the personal CRUD api project using python web framework django.__

### Built With

* [Django](https://www.djangoproject.com/)

### Prerequisites

* Python 3.8 or higher
    ```sh
    python --version
    ```
* poetry install  
    - If you want to use the poetry tool, install it from the link below.  
    ```sh
    https://python-poetry.org/docs/
    ```
    - after install, set the below on the bash or zsh and so on  
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
   poetry add `cat requirements.txt`
   ```
   or not
   ```sh
   pip install -r requirements.txt
   ```

<!-- USAGE EXAMPLES -->
### Usage

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

<!-- LICENSE -->
## License

Distributed under the DSF License. See `LICENSE` for more information.