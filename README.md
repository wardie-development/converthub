# ConvertHub

## Description

A simple application to convert files from one format to another, 
and to resize images to different sizes. 

## Introduction

1. Clone the repo and create your virtual environment.
2. Run `make build` command.
3. Run `make test` command to run the tests. The coverage must be 100%.
4. Run `make run` command to run the application.
5. Run `curl -X GET http://localhost:8000/healthcheck` to check if the application is running.

> You can run `make run port=<port>`, 
> where `<port>` is the port number you want to run the application on. 
> Default is 8000 


## Endpoints

base_url = `...`

### POST `base_url`/convert/{from}/{to}

> Example: from = `html`, to = `pdf`

#### Request

```json
{
  "file_content": "...",  // base64 encoded
  "file_name": "test.html" // optional
}
```

#### Response

200 OK:
```json
{
  "file_name": "test.pdf",
  "file_content": "...",  // base64 encoded
  "file_type": "pdf",
  "entity_id": "fdca6269-75dc-42a7-8371-a77b91525cf7"
}
```

Any Status different from 200 OK:
```json
{
  "code": 123,
  "message": "..."
}
```

### POST `base_url`/resize

#### Request

```json
{
  "file_content": "...",  // base64 encoded
  "file_name": "test.png", // optional
  "file_type": "png",
  "sizes": [
    {
      "width": 100,
      "height": 100
    },
    {
      "width": 200,
      "height": 200
    },
    {
      "width": 200,
      "height": 200
    }
  ]
}
```

#### Response

200 OK:
```json
{
  "resized_images": [
    {
      "file_name": "100x100_test.png",
      "file_content": "...", // base64 encoded
      "file_type": "png",
      "entity_id": "c46d7b21-8482-4e64-b912-c75af810e051",
      "size": {
        "width": 100,
        "height": 100
      }
    },
    {
      "file_name": "200x200_test.png",
      "file_content": "...",  // base64 encoded
      "file_type": "png",
      "entity_id": "194777e9-fa53-4752-b199-8fc5996e8f30",
      "size": {
        "width": 200,
        "height": 200
      }
    }
  ]
}
```

> Note: Repeated sizes will be ignored


Any Status different from 200 OK:
```json
{
  "code": 123,
  "message": "..."
}
```


### GET `base_url`/healthcheck

#### Response

200 OK:
```json
{
	"status": "success",
	"data": "ok"
}
```
