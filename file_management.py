from flask import send_file, request, redirect, url_for, flash
from io import BytesIO
import os
import tempfile
import pandas as pd
from data_processing import handle_missing_values

def export_file():
    # Đọc toàn bộ file Excel từ thư mục 'data'
    excel_path = 'data/SampleData.xlsx'
    if not os.path.exists(excel_path):
        return "File không tồn tại", 404

    # Đọc tất cả các sheet từ file Excel
    data = pd.read_excel(excel_path, sheet_name=None)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='data.xlsx'
    )



def import_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    
    if file and file.filename.endswith('.xlsx'):
        # Lưu file vào đường dẫn tạm thời
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, 'temp_data.xlsx')
        file.save(temp_path)
        
        # Di chuyển file từ đường dẫn tạm thời vào thư mục đích
        final_path = os.path.join('data', 'data.xlsx')
        if not os.path.exists('data'):
            os.makedirs('data')
        if os.path.exists(final_path):
            os.remove(final_path)
        os.rename(temp_path, final_path)
        
        # Xử lý giá trị thiếu trong tệp Excel
        handle_missing_values(final_path)
        
        flash('File uploaded and processed successfully', 'success')
        return redirect(url_for('index'))
    
    flash('Invalid file type', 'error')
    return redirect(url_for('index'))