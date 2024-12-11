import pandas as pd
import numpy as np

def class_grades(students):
    
    df = pd.DataFrame(students, columns=['Name', 'Class', 'Grade'])
    
    median_grades = df.groupby('Class')['Grade'].median().reset_index()
    
    result = median_grades.values.tolist()
    
    return result

students = [["Ana Stevens", "1a", 5], ["Mark Stevens", "1a", 4], ["Jon Jones", "1a", 2], ["Bob Kent", "1b", 4]]
print(class_grades(students))