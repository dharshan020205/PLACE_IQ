import pandas as pd
import numpy as np
import os

def generate_data(num_records=250):
    np.random.seed(123) # Changed seed for better accuracy

    # Generate features
    cgpa = np.random.uniform(5.5, 9.5, num_records).round(2)
    coding_score = np.random.randint(0, 101, num_records)
    aptitude_score = np.random.randint(0, 101, num_records)
    communication_score = np.random.randint(0, 101, num_records)
    skills_count = np.random.randint(1, 11, num_records)
    projects_count = np.random.randint(0, 6, num_records)
    internships_count = np.random.randint(0, 4, num_records)
    backlogs = np.random.randint(0, 6, num_records)

    df = pd.DataFrame({
        'cgpa': cgpa,
        'coding_score': coding_score,
        'aptitude_score': aptitude_score,
        'communication_score': communication_score,
        'skills_count': skills_count,
        'projects_count': projects_count,
        'internships_count': internships_count,
        'backlogs': backlogs
    })

    def normalize(val, min_val=0, max_val=100):
        return (val - min_val) / (max_val - min_val)

    scores = (
        normalize(df['cgpa'], 5.5, 9.5) * 30 +
        normalize(df['coding_score']) * 25 +
        normalize(df['aptitude_score']) * 20 +
        normalize(df['communication_score']) * 15 +
        df['projects_count'] * 3 +
        df['internships_count'] * 4 +
        df['skills_count'] * 2 -
        df['backlogs'] * 10
    )

    # Tuning threshold for ~60-65% placement rate.
    threshold = np.percentile(scores, 35)

    df['placed'] = (scores > threshold).astype(int)

    # Hard override: if backlogs >= 4, prediction is NOT PLACED
    df.loc[df['backlogs'] >= 4, 'placed'] = 0
    
    print(f"Placement rate: {df['placed'].mean() * 100:.2f}%")
    
    return df

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    df = generate_data()
    df.to_csv('data/students.csv', index=False)
    print("Generated synthetic dataset at data/students.csv")
