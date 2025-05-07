from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.model_selection import train_test_split
from flask_mysqldb import MySQL


app = Flask(__name__)

# Configure the database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database_name'
mysql = MySQL(app)

# Define the database model
# class HouseRent:
#     def __init__(self, rent_details):
        # Initialize the model with rent details
        # Set other attributes as per your requirements

# Load and preprocess the data
data = pd.read_csv("D:/Users/91978/Downloads/House_rent_sample.csv")
        # Preprocess code...
data["Area Type"] = data["Area Type"].map({"Super Area": 1, "Carpet Area": 2, "Built Area": 3})
data["City"] = data["City"].map({"Mumbai": 4000, "Chennai": 6000, "Bangalore": 5600, "Hyderabad": 5000, "Delhi": 1100, "Kolkata": 7000})
data["Furnishing Status"] = data["Furnishing Status"].map({"Unfurnished": 0, "Semi-Furnished": 1, "Furnished": 2})
data["Tenant Preferred"] = data["Tenant Preferred"].map({"Bachelors/Family": 2, "Bachelors": 1, "Family": 3})

x = np.array(data[["BHK", "Size", "Area Type", "City", "Furnishing Status", "Tenant Preferred", "Bathroom"]])
y = np.array(data[["Rent"]])

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.10, random_state=42)

# Build the model
# Model code...
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(xtrain.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(xtrain, ytrain, batch_size=1, epochs=21)
# Route for saving rent details
@app.route('/save_rent', methods=['POST'])
def save_rent():
    # Extract the rent details from the form submission
    rent_details = {
        'bhk': request.form.get('bhk'),
        'size': request.form.get('size'),
        'area_type': request.form.get('area_type'),
        'pincode': request.form.get('pincode'),
        'furnishing': request.form.get('furnishing'),
        'tenant_type': request.form.get('tenant_type'),
        'bathrooms': request.form.get('bathrooms'),
        # Add more rent details fields as per your form
    }

    # Create a new HouseRent instance with the rent details
    new_rent = HouseRent(rent_details)

    # Save the rent details to the database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO house_rent (bhk, size, area_type, pincode, furnishing, tenant_type, bathrooms) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (new_rent.bhk, new_rent.size, new_rent.area_type, new_rent.pincode, new_rent.furnishing, new_rent.tenant_type, new_rent.bathrooms))
    mysql.connection.commit()
    cur.close()

    # Retrieve all rent details from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM house_rent")
    all_rent = cur.fetchall()
    cur.close()

    # Update the dataset with the latest rent details
    x_updated = np.array([list(rent[1:]) for rent in all_rent])
    y_updated = np.array([rent[2] for rent in all_rent])

    # Retrain the model with the updated dataset
    model.fit(x_updated, y_updated, batch_size=1, epochs=21)

    return 'Rent details saved successfully.'

# Route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_price = None
    if request.method == 'POST':
        # Predict price code...
        bhk = request.form.get('bhk')
        size = request.form.get('size')
        area_type = request.form.get('area_type')
        pincode = request.form.get('pincode')
        furnishing = request.form.get('furnishing')
        tenant_type = request.form.get('tenant_type')
        bathrooms = request.form.get('bathrooms')
        features = np.array([[bhk, size, area_type, pincode, furnishing, tenant_type, bathrooms]], dtype=int)
        predicted_price = model.predict(features)[0][0]
    return render_template('index.html', predicted_price=predicted_price)

if __name__ == '__main__':
    app.run()
