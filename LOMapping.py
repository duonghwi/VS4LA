import pandas as pd


def get_assignment_labels(file_path):
    aqlo_df = pd.read_excel(file_path, sheet_name='AQLOAlignment')
    lo_description_df = pd.read_excel(file_path, sheet_name='LO Description')
    lo_description_dict = dict(zip(lo_description_df['LO'], lo_description_df['LO Description']))
    
    assignment_labels = {}
    for index, row in aqlo_df.iterrows():
        activity = row['Activity']
        lo = row['LO']
        lo_desc = lo_description_dict.get(lo, '')
        assignment_labels[activity] = f"{activity} - {lo_desc}"
    
    return assignment_labels


def get_exam_lo_mapping(file_path):
    lo_alignment = pd.read_excel(file_path, sheet_name='ExamLOAlignment')
    lo_description = pd.read_excel(file_path, sheet_name='LO Description')
    lo_desc_mapping = pd.Series(lo_description['LO Description'].values, index=lo_description['LO']).to_dict()
    
    question_label_mapping = {}
    for _, row in lo_alignment.iterrows():
        lo = row['LO']
        question = row['Question of final exam']
        if lo in lo_desc_mapping:
            question_label_mapping[question] = f"{question} - {lo_desc_mapping[lo]}"
    
    return question_label_mapping
