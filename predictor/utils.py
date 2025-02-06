import pickle
import json
import numpy as np
import os

__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def get_location_names():
    load_saved_artifacts()  # Ensure data is loaded
    if __locations is None:
        raise Exception(
            "Locations not loaded. Check if artifacts are present and accessible."
        )
    return __locations


def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    # Only load if not already loaded
    if __data_columns is None:
        try:
            artifacts_path = os.path.join(os.path.dirname(__file__), "artifacts")

            columns_path = os.path.join(artifacts_path, "columns.json")
            model_path = os.path.join(
                artifacts_path, "banglore_home_prices_model.pickle"
            )

            print(f"Loading artifacts from: {artifacts_path}")  # Debug print

            if not os.path.exists(columns_path):
                raise FileNotFoundError(f"columns.json not found at {columns_path}")

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"model pickle not found at {model_path}")

            with open(columns_path, "r") as f:
                __data_columns = json.load(f)["data_columns"]
                __locations = __data_columns[3:]
                print(f"Loaded {len(__locations)} locations")  # Debug print

            with open(model_path, "rb") as f:
                __model = pickle.load(f)
                print("Model loaded successfully")  # Debug print

        except Exception as e:
            print(f"Error loading artifacts: {str(e)}")
            raise
