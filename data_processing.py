import pandas as pd
import numpy as np
from LOMapping import get_exam_lo_mapping

def read_data(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def handle_missing_values(filepath):
    sheets = pd.read_excel(filepath, sheet_name=None)
    for sheet_name, df in sheets.items():
        df.replace(['-', 'null', 'NaN', np.nan, None], np.nan, inplace=True)
        df.fillna(0, inplace=True)

    with pd.ExcelWriter(filepath, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)


#COURSE ANALYSIS

def calculate_statistics(df):
    if 'Final Note' in df.columns:
        grades = df['Final Note'].dropna()
        excellent = grades[grades >= 9].count()
        good = grades[(grades >= 7) & (grades < 9)].count()
        average = grades[(grades >= 5) & (grades < 7)].count()
        fail = grades[grades < 5].count()
        total = excellent + good + average + fail
        
        return {
            'Excellent': excellent / total * 100,
            'Good': good / total * 100,
            'Average': average / total * 100,
            'Fail': fail / total * 100
        }
    else:
        return {
            'Excellent': 0,
            'Good': 0,
            'Average': 0,
            'Fail': 0
        }

def get_histogram_data(file_path):

    df = read_data(file_path, 'Final Note')
    data = df['Final Note']
    bins = [i for i in range(0, 11)]  
    bins[-1] += 0.1  
    categorized_data = pd.cut(data, bins=bins, right=False, include_lowest=True)
    hist = categorized_data.value_counts(sort=False)
    bin_labels = [f'{bins[i]}-{bins[i+1] - 0.1}' for i in range(len(bins) - 1)]
    if len(hist) < len(bin_labels):
        hist = hist.reindex(bin_labels, fill_value=0)
    return {'bins': bin_labels, 'counts': hist.tolist()}


#ASSIGNMENT ANALYSIS

def get_assignment_scores(file_path):
    df = read_data(file_path, 'Assignment Sample Data')
    
    assignment_columns = [col for col in df.columns if col.startswith('A')]
    scores = {col: df[col].dropna().tolist() for col in assignment_columns}
    
    return scores

def get_assignment_histogram_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Assignment Sample Data')
    
    assignment_columns = [col for col in df.columns if col != 'Username']
    
    histogram_data = {}
    for col in assignment_columns:
        bins = pd.cut(df[col].dropna(), bins=range(0, 12, 2), right=False)
        histogram_data[col] = bins.value_counts(sort=False).tolist()
    
    bin_labels = [f'{i}-{i+2}' for i in range(0, 10, 2)]
    
    return {'bins': bin_labels, 'histogram_data': histogram_data}




#QUIZ ANALYSIS 



def get_quiz_data(file_path):
    # Đọc dữ liệu từ sheet "Quiz Sample Data"
    df = pd.read_excel(file_path, sheet_name='Quiz Sample Data')

    # Lấy tất cả các cột có tiêu đề bắt đầu bằng 'Q.'
    quiz_columns = [col for col in df.columns if col.startswith('Q.')]

    # Tính toán số lượng đúng/sai cho mỗi cột 'Q.'
    result = {col.split()[0]: df[col].dropna().value_counts().reindex([0, 1], fill_value=0).tolist() for col in quiz_columns}

    return result

#EXAM ANALYSI

def get_exam_scores(file_path):
    # Read the final note data
    exam_data = read_data(file_path, 'Final Exam Sample Data')
    question_label_mapping = get_exam_lo_mapping(file_path)
  
    data = {}
    for question in question_label_mapping.keys():
        if question in exam_data.columns:
            data[question_label_mapping[question]] = exam_data[question].dropna().tolist()
    
    return data


def get_exam_summary(file_path):
    lo_mapping = get_exam_lo_mapping(file_path)
    df = pd.read_excel(file_path, sheet_name='Final Exam Sample Data')

    columns = [col for col in df.columns if col.startswith('Q')]

    summary = {}
    for col in columns:
        if col in lo_mapping:  
            summary[lo_mapping[col]] = {
                'min': int(df[col].min()),
                'max': int(df[col].max()),
                'avg': float(df[col].mean())
            }
    
    return summary

def get_exam_histogram_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Final Exam Sample Data')
    exam_columns = [col for col in df.columns if col.startswith('Q')]
    histogram_data = {}
    for col in exam_columns:
        bins = pd.cut(df[col].dropna(), bins=range(0, 12, 2), right=False)
        histogram_data[col] = bins.value_counts(sort=False).tolist()
    
    bin_labels = [f'{i}-{i+2}' for i in range(0, 10, 2)]
    
    return {'bins': bin_labels, 'histogram_data': histogram_data}




#Learner Analysis



def get_student_list(file_path):
    final_note_df = pd.read_excel(file_path, sheet_name='Final Note')
    return final_note_df['MSSV'].tolist()

def get_assignment_scores(file_path):
    df = read_data(file_path, 'Assignment Sample Data')
    assignment_scores = {col: df[col].tolist() for col in df.columns if col.startswith('A')}
    return assignment_scores

def get_class_average_scores(file_path):
    df_final_note = read_data(file_path, 'Final Note')
    df_assignment = read_data(file_path, 'Assignment Sample Data')
    df_quiz = read_data(file_path, 'Quiz Sample Data')

    final_note_avg = df_final_note['Final Note'].mean()
    final_exam_avg = df_final_note['Final Exam'].mean()
    quiz_avg = df_quiz['Grade/20.00'].mean()
    assignment_avgs = {col: df_assignment[col].mean() for col in df_assignment.columns if col.startswith('A')}

    return {
        'Final Note': final_note_avg.item(),  
        'Final Exam': final_exam_avg.item(),
        'Quiz': quiz_avg.item(),
        'Assignments': {col: avg.item() for col, avg in assignment_avgs.items()},
        
    }

def get_student_scores(file_path, username):
    df_final_note = read_data(file_path, 'Final Note')
    df_assignment = read_data(file_path, 'Assignment Sample Data')
    df_quiz = read_data(file_path, 'Quiz Sample Data')

    student_final_note = df_final_note.loc[df_final_note['MSSV'] == username, 'Final Note'].values[0]
    student_final_exam = df_final_note.loc[df_final_note['MSSV'] == username, 'Final Exam'].values[0]
    student_quiz = df_quiz.loc[df_quiz['Username'] == username, 'Grade/20.00'].values[0]
    student_assignments = {col: df_assignment.loc[df_assignment['Username'] == username, col].values[0] for col in df_assignment.columns if col.startswith('A')}

    return {
        'Final Note': student_final_note.item(),  
        'Final Exam': student_final_exam.item(),
        'Quiz': student_quiz.item(),
        'Assignments': {col: score.item() for col, score in student_assignments.items()}
    }
