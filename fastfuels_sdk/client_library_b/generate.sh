# Delete old code
rm -r api/ models/ __init__.py api_client.py api_response.py configuration.py exceptions.py py.typed rest.py

PACKAGE_NAME=client_library_b

curl https://api.fastfuels.silvxlabs.com/openapi.json > api_spec.json

openapi-generator generate -i api_spec.json -g python -o ./python_client --package-name $PACKAGE_NAME

mv python_client/$PACKAGE_NAME/* .

rm -r python_client/ api_spec.json
