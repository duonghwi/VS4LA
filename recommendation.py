import pandas as pd


def count_score_ranges(file_path):
    # Đọc dữ liệu từ file Excel
    df = pd.read_excel(file_path,sheet_name='Quiz Sample Data')

    # Lọc cột điểm (Grade/20.00)
    scores = df['Grade/20.00']

    # Khởi tạo biến đếm cho từng khoảng điểm
    count_ranges = {
        '0 điểm': 0,
        '1 đến 2 điểm': 0,
        '3 đến 4 điểm': 0,
        '5 đến 6 điểm': 0,
        '7 đến 8 điểm': 0,
        '9 đến 10 điểm': 0,
        '11 đến 12 điểm': 0,
        '13 đến 14 điểm': 0,
        '15 đến 16 điểm': 0,
        '17 đến 18 điểm': 0,
        '19 đến 20 điểm': 0,
    }

    # Đếm số lượng trong từng khoảng điểm
    for score in scores:
        if score == 0:
            count_ranges['0 điểm'] += 1
        elif 1 <= score <= 2:
            count_ranges['1 đến 2 điểm'] += 1
        elif 3 <= score <= 4:
            count_ranges['3 đến 4 điểm'] += 1
        elif 5 <= score <= 6:
            count_ranges['5 đến 6 điểm'] += 1
        elif 7 <= score <= 8:
            count_ranges['7 đến 8 điểm'] += 1
        elif 9 <= score <= 10:
            count_ranges['9 đến 10 điểm'] += 1
        elif 11 <= score <= 12:
            count_ranges['11 đến 12 điểm'] += 1
        elif 13 <= score <= 14:
            count_ranges['13 đến 14 điểm'] += 1
        elif 15 <= score <= 16:
            count_ranges['15 đến 16 điểm'] += 1
        elif 17 <= score <= 18:
            count_ranges['17 đến 18 điểm'] += 1
        elif 19 <= score <= 20:
            count_ranges['19 đến 20 điểm'] += 1

    # Trả về kết quả đếm
    return count_ranges

# Ví dụ sử dụng hàm
file_path = 'data/data.xlsx'
result = count_score_ranges(file_path)
print(result)