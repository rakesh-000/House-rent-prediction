import subprocess
from flask import Flask, render_template, request, render_template_string
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
# from sklearn.model_selection import train_test_split # type: ignore

app = Flask(__name__)

# Load and preprocess the data
<<<<<<< HEAD
# data = pd.read_csv("C:/Users/91978/project/github/HouseRent-Prediction/House_rent/Houserent.csv")
=======
data = pd.read_csv("C:/Users/User/Documents/GitHub/HouseRent-Prediction/House_rent/Houserent.csv")
>>>>>>> e9d9b2b7bf709696982f4c1fa0595af29946be62

data["Area Type"] = data["Area Type"].map({"Super Area": 1, "Carpet Area": 2, "Built Area": 3})
data["City"] = data["City"].map({"Mumbai": 4000, "Chennai": 6000, "Bangalore": 5600, "Hyderabad": 5000, "Delhi": 1100, "Kolkata": 7000})
data["Furnishing Status"] = data["Furnishing Status"].map({"Unfurnished": 0, "Semi-Furnished": 1, "Furnished": 2})
data["Tenant Preferred"] = data["Tenant Preferred"].map({"Bachelors/Family": 2, "Bachelors": 1, "Family": 3})

x = np.array(data[["BHK", "Size", "Area Type", "City", "Furnishing Status", "Tenant Preferred", "Bathroom"]])
y = np.array(data[["Rent"]])

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.10, random_state=42)

# Build the model
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(xtrain.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(xtrain, ytrain, batch_size=1, epochs=21)




@app.route('/prediction', methods=['GET', 'POST'])
def index():
    return render_template('predict.html')

@app.route('/index', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/details', methods=['GET', 'POST'])
def details():
    return render_template('details.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/', methods=['GET', 'POST'])
def open():
    predicted_price = None
    if request.method == 'POST':
        bhk = float(request.form.get('bhk'))
        size = float(request.form.get('size'))
        area_type = float(request.form.get('area_type'))
        pincode = float(request.form.get('pincode'))
        furnishing = float(request.form.get('furnishing'))
        tenant_type = float(request.form.get('tenant_type'))
        bathrooms = float(request.form.get('bathrooms'))
        features = np.array([[bhk, size, area_type, pincode, furnishing, tenant_type, bathrooms]], dtype=float)
        predicted_price = model.predict(features)[0][0]

    return render_template('index.html', predicted_price=predicted_price)



if __name__ == '__main__':
    app.run()

# {% if predicted_price is defined %}
#                 <p>Predicted Rent: {{ predicted_price }}</p>
#             {% endif %}