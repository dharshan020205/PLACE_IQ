import sys
import os

# Add the parent directory to the path so we can import 'backend'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import predict_placement, StudentFeatures

def test_predict_success():
    features = StudentFeatures(
        cgpa=8.5,
        coding_score=85,
        aptitude_score=80,
        communication_score=75,
        skills_count=5,
        projects_count=2,
        internships_count=1,
        backlogs=0
    )
    result = predict_placement(features)
    print("Success Case:", result)

def test_predict_override():
    features = StudentFeatures(
        cgpa=8.5,
        coding_score=85,
        aptitude_score=80,
        communication_score=75,
        skills_count=5,
        projects_count=2,
        internships_count=1,
        backlogs=5
    )
    result = predict_placement(features)
    print("Override Case:", result)

if __name__ == "__main__":
    test_predict_success()
    test_predict_override()
