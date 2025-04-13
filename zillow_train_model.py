import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

# Load your Zillow dataset
df = pd.read_excel(r"C:\Users\Vidhya\Desktop\zillow home project\Zillow_Project\Zillow House Price Prediction Data.xlsx")


  # Replace with your actual CSV file name

# Select relevant features
features = ['bedrooms', 'bathrooms', 'livingArea', 'yearBuilt']
target = 'price'

# Drop missing values
df = df[features + [target]].dropna()

# Split
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Save
with open("zillow_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as 'zillow_model.pkl'")
