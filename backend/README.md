### Test the API

# Run the server
```bash
$ python api.py
```
- Send a `POST` request to `/predict` with `image` argument containing the `base64` image string

> `POST http://127.0.0.1:5000/predict?image={{base64_string}}`

- The response will be a string

#### Use this [website](https://base64.guru/converter/encode/image) to convert images to base64
