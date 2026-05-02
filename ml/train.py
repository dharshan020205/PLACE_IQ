import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import json
from datetime import datetime

def train_model():
    data_path = 'data/students.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run data_generator.py first.")
        return
    
    df = pd.read_csv(data_path)
    
    X = df.drop('placed', axis=1)
    y = df['placed']
    
    # 80/20 split as per spec
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Logistic Regression model
    model = LogisticRegression(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {acc:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Print Feature coefficients for debugging/verification
    coefficients = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_[0]
    }).sort_values(by='Coefficient', ascending=False)
    print("\nFeature Coefficients:")
    print(coefficients)
    
    # Save artifacts
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/logistic_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    # Save model metadata
    model_info = {
        "version": "1.0",
        "accuracy": acc,
        "last_trained_date": datetime.now().isoformat(),
        "feature_names": list(X.columns)
    }
    with open('models/model_info.json', 'w') as f:
        json.dump(model_info, f)
        
    print("\nModel and scaler saved to models/")

if __name__ == '__main__':
    train_model()
