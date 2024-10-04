from flask import Flask, render_template, jsonify
import file_management as fm
import data_processing as dp
import LOMapping as lm
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

@app.route('/')
def index():
    return render_template('FileManager.html')

@app.route('/download')
def download_file():
    return fm.export_file()


@app.route('/upload', methods=['POST'])
def upload_file():
    return fm.import_file()


#Course_analysis
def get_statistics():
    df = dp.read_data('data/data.xlsx', 'Final Note')
    return dp.calculate_statistics(df)

@app.route('/course-analysis')
def course_analysis():
    data = get_statistics()
    return render_template('course_analysis.html', data=data)

@app.route('/api/course-analysis-data')
def course_analysis_data():
    data = get_statistics()
    return jsonify(data)

@app.route('/api/histogram-data')
def histogram_data():
    data = dp.get_histogram_data('data/data.xlsx')
    return jsonify(data)

@app.route('/api/boxplot-data')
def boxplot_data():
    file_path = 'data/data.xlsx'
    df = dp.read_data(file_path, 'Final Note')
    
    # Extract the relevant columns
    data = {
        'LAB': df['LAB'].dropna().tolist(),
        'BONUS': df['BONUS'].dropna().tolist(),
        'Assignment-Quiz': df['Assignment-Quiz'].dropna().tolist(),
        'Final Exam': df['Final Exam'].dropna().tolist()
    }
    
    return jsonify(data)



#Assignment analysis
@app.route('/assignment_analysis')
def assignment_analysis():
    return render_template('assignment_analysis.html')
    

@app.route('/api/assignment-analysis-data')
def assignment_analysis_data():
    file_path = 'data/data.xlsx'  
    df = dp.read_data(file_path, sheet_name='Assignment Sample Data')
    assignment_labels = lm.get_assignment_labels(file_path)
    
    
    data = {}
    for col in df.columns[1:]: 
        if col in assignment_labels:
            data[assignment_labels[col]] = df[col].dropna().tolist()
    
    return jsonify(data)


@app.route('/api/assignment-histogram-data')
def assignment_histogram_data():
    file_path = 'data/data.xlsx'  
    data = dp.get_assignment_histogram_data(file_path)
    return jsonify(data)


#Quiz analysis
@app.route('/quiz_analysis')
def quiz_analysis():
    return render_template('quiz_analysis.html')

@app.route('/api/quiz-analysis-data')
def quiz_analysis_data():
    file_path = 'data/data.xlsx'
    quiz_data = dp.get_quiz_data(file_path)  
    return jsonify(quiz_data)







#Exam analysis
@app.route('/exam_analysis')
def exam_analysis():
    return render_template('exam_analysis.html')

@app.route('/api/exam-analysis-data')
def exam_analysis_data():
    data = dp.get_exam_scores('data/data.xlsx')
    return jsonify(data)

@app.route('/api/exam-summary-data')
def exam_summary_data():
    data = dp.get_exam_summary('data/data.xlsx')
    return jsonify(data)

@app.route('/api/exam_histogram_data')
def exam_histogram_data():
    data = dp.get_exam_histogram_data('data/data.xlsx')
    return jsonify(data)

#Learner Analysis
@app.route('/learner-analysis')
def learner_analysis():
    return render_template('learner_analysis.html')

@app.route('/api/student-list')
def student_list():
    file_path = 'data/data.xlsx'
    students = dp.get_student_list(file_path)
    return jsonify(students)

@app.route('/api/learner-analysis-data/<username>')
def learner_analysis_data(username):
    file_path = 'data/data.xlsx'
    student_scores = dp.get_student_scores(file_path, username)
    class_averages = dp.get_class_average_scores(file_path)
    return jsonify({
        'student_scores': student_scores,
        'class_averages': class_averages
    })




if __name__ == '__main__':
    app.run(debug=True)
