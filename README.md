# years-of-service-award
Overlays images

## Dependencies
### Services
  - Redis server >= 5.0.7
### Python packages
Developed on Python 3.8.10.  Python package requirements for this project a provided in `requirements.txt`.

    php install -r requirements.txt

## Configuration
This application will attempt to read the following environment variables to configure its input and output directories.  If those values are not found then it will attempt to find those directories in the script directory.

    YOSA_INPUT_DIR
    YOSA_OUTPUT_DIR

