import joblib
import json
import os
import numpy as np

class ModelService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, 'models')
        
        self.model = joblib.load(os.path.join(models_dir, 'logistic_model.pkl'))
        self.scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
        
        with open(os.path.join(models_dir, 'model_info.json'), 'r') as f:
            self.model_info = json.load(f)
            
        self.feature_names = self.model_info.get('feature_names', [
            'cgpa', 'coding_score', 'aptitude_score', 'communication_score', 
            'skills_count', 'projects_count', 'internships_count', 'backlogs'
        ])
        
        # Calculate feature weights for explainability
        coeffs = self.model.coef_[0]
        self.feature_weights = {name: float(coef) for name, coef in zip(self.feature_names, coeffs)}

    def get_model_info(self):
        return self.model_info

    def predict(self, feature_dict: dict):
        # 1. Input validation & vectorization
        feature_vector = np.array([[feature_dict[name] for name in self.feature_names]])
        
        # 2. Rule engine check (backlogs >= 4 -> override)
        backlogs = feature_dict.get('backlogs', 0)
        rule_override = False
        
        # 3. Model Inference
        scaled_vector = self.scaler.transform(feature_vector)
        probability = float(self.model.predict_proba(scaled_vector)[0][1])
        
        if backlogs >= 4:
            rule_override = True
            probability = 0.0 # Force to 0 for overriding prediction
            
        prediction_label = "Likely to be placed" if probability >= 0.5 else "Likely NOT placed"
        if rule_override:
             prediction_label = "NOT PLACED (Rule Override: Backlogs >= 4)"

        # 4. Confidence banding (< 0.55 = low, 0.55-0.75 = medium, > 0.75 = high)
        if probability < 0.55:
            confidence_band = "low"
        elif probability <= 0.75:
            confidence_band = "medium"
        else:
            confidence_band = "high"
            
        if rule_override:
            confidence_band = "high" # Highly confident they won't be placed
            
        return {
            "prediction": prediction_label,
            "probability": round(probability, 4),
            "rule_override": rule_override,
            "confidence_band": confidence_band,
            "feature_weights": self.feature_weights
        }

model_service = ModelService()
