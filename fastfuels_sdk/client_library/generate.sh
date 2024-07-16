# Generate the client library using openapi-python-client
# openapi-python-client generate --url https://api-prod-nyvjyh5ywa-uw.a.run.app/openapi.json --overwrite
openapi-python-client generate --url http://127.0.0.1:8080/openapi.json --overwrite


# Move the contents of the fast-fuels-api-client/fast_fuels_api_client directory to the current directory
mv fast-fuels-api-client/fast_fuels_api_client/* .

# Move the README.md file to the current directory
mv fast-fuels-api-client/README.md .

# Remove the fast-fuels-api-client directory
rm -r fast-fuels-api-client
