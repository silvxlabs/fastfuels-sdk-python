# Remove old code
rm -r api/ models/ __init__.py client.py errors.py py.typed README.md types.py

PACKAGE_NAME=client_library_a

# Generate the client library using openapi-python-client
openapi-python-client generate --url https://api.fastfuels.silvxlabs.com/openapi.json --config config.yaml

# Move the contents of the fast-fuels-api-client/fast_fuels_api_client directory to the current directory
mv fast-fuels-api-client/$PACKAGE_NAME/* .

# Move the README.md file to the current directory
mv fast-fuels-api-client/README.md .

# Remove the fast-fuels-api-client directory
rm -r fast-fuels-api-client
