# Python client for Acquia Content Hub

content_hub_python is a package that helps you connect to Acquia Content Hub.

## Install

```bash
    pip install content_hub_python
```

## Usage

To register a client you can do the following:
```python
    try:
        myclient = plexus.register_client("myclient")
    except HttpError as e:
        print("Could not register client. Status code:", e.response.status_code)
```
