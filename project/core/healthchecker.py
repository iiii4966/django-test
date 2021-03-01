import requests


def check_health():
    # Enhance
    response = requests.get("http://0.0.0.0:8000")
    if response.status_code == 500:
        response.raise_for_status()


if __name__ == '__main__':
    check_health()