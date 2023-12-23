from chalice import CORSConfig

cors = CORSConfig(
    allow_origin="*",
    allow_headers=[
        "Content-Type",
        "X-Amz-Date",
        "Authorization",
        "X-Api-Key",
        "X-Amz-Security-Token",
        "Content-Range",
    ],
    expose_headers=["Content-Range"],
)
