# curl https://api.fastfuels.silvxlabs.com/openapi.json > api_spec.json
curl http://127.0.0.1:8080/openapi.json > api_spec.json

openapi-generator generate -i api_spec.json -g python -o ./python_client
