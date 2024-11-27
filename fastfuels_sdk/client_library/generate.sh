rm -r api/ models/ __init__.py api_client.py api_response.py configuration.py exceptions.py py.typed rest.py

PACKAGE_NAME="client_library"

curl https://api.fastfuels.silvxlabs.com/openapi.json > api_spec.json

openapi-generator generate -i api_spec.json -g python -o ./python_client --package-name $PACKAGE_NAME

mv python_client/$PACKAGE_NAME/* .

# Fix imports, targeting specific files to ensure complete coverage
for file in api_client.py rest.py api_response.py configuration.py exceptions.py; do
    perl -pi -e 's/from client_library/from fastfuels_sdk.client_library/g' $file
    perl -pi -e 's/import client_library/import fastfuels_sdk.client_library/g' $file
done

# Fix remaining imports
find . -type f -name "*.py" -exec perl -pi -e 's/fastfuels_sdk\.fastfuels_sdk\./fastfuels_sdk./g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/from client_library\./from fastfuels_sdk.client_library./g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/import client_library\./import fastfuels_sdk.client_library./g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/(?<![\.])(client_library\.models)/fastfuels_sdk.$1/g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/(?<![\.])(client_library\.api\.)/fastfuels_sdk.$1/g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/(?<![\.])(client_library\.api_client)/fastfuels_sdk.$1/g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/(?<![\.])(client_library\.rest)/fastfuels_sdk.$1/g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/(?<![\.])(client_library\.api_response)/fastfuels_sdk.$1/g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/(?<![\.])(client_library\.configuration)/fastfuels_sdk.$1/g' {} +
find . -type f -name "*.py" -exec perl -pi -e 's/(?<![\.])(client_library\.exceptions)/fastfuels_sdk.$1/g' {} +

rm -r python_client/ api_spec.json