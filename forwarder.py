from flask import Flask
import requests
import configparser
from utils.file_utils import load_properties

app = Flask(__name__)

# Load configurations from properties file
config = load_properties();

FORWARD_URL = config.get('FORWARD_URL').data
SECONDARY_URL = config.get('SECONDARY_URL').data
TOP_MOVIES = config.get('TOP_MOVIES').data
AB_TEST = config.get('AB_TEST').data

# print(FORWARD_URL)
# print(SECONDARY_URL)
# print(TOP_MOVIES)
print(AB_TEST)

@app.route('/recommend/<userId>')
def recommend(userId):
    try:
        config = load_properties();
        # Determine URL based on AB testing switch and userId
        url_to_use = config.get('FORWARD_URL').data
        if config.get('AB_TEST').data == 'ON':
            if int(userId) % 2 == 0:  # Even userId
                print("Using Secondary URL")
                url_to_use = config.get('SECONDARY_URL').data
        response = requests.get(f"{url_to_use}/{userId}", timeout=0.4)

        if response.status_code == 200:
            return response.text
        else:
            print("Status_code:", response.status_code)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, ValueError):
        print("Took Long or Invalid UserId")
        pass

    return TOP_MOVIES


if __name__ == '__main__':
    app.run(debug=True, port=8082, host='0.0.0.0')
