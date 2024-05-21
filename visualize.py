from time import sleep
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_top_words(df):
    # Lấy danh sách các nhãn (labels)
    labels = df['Predicted_Label'].unique()

    # Tạo hình vẽ chứa nhiều biểu đồ cột
    fig, axes = plt.subplots(len(labels), figsize=(8, 6 * len(labels)))

    # Lặp qua từng nhãn và vẽ biểu đồ tương ứng
    for i, label in enumerate(labels):
        # Lấy dữ liệu của nhãn hiện tại
        label_data = df[df['Predicted_Label'] == label]

        # Tạo từ điển để đếm tần suất xuất hiện của các từ
        word_counts = {}
        for content in label_data['Content']:
            words = content.split()
            for word in words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

        # Sắp xếp từ điển theo giá trị tần suất giảm dần
        sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

        # Lấy top 5 từ xuất hiện nhiều nhất
        top_words = sorted_counts[:20]
        top_words = dict(top_words)

        # Vẽ biểu đồ cột trên các trục tương ứng
        ax = axes[i]
        ax.bar(top_words.keys(), top_words.values())
        ax.set_title(f"Top 20 words - Label: {label}")
        ax.set_xlabel("Word")
        ax.set_ylabel("Frequency")
        ax.tick_params(axis='x', rotation=45)

    # Tạo khoảng trống giữa các biểu đồ
    plt.tight_layout()

    # Hiển thị hình vẽ chứa các biểu đồ cột
    return fig
# Định nghĩa hàm để đọc file .csv và trả về DataFrame
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Đường dẫn tới file .csv
csv_file_path = "E:\HK5\CongNgheDuLieuLon\DoAn\VnCoreNLP/result.csv"

# Đọc file .csv ban đầu
df = read_csv(csv_file_path)
df = df.dropna()
# Tạo ứng dụng Streamlit
st.title("Continuous CSV Reader")
st.write("Real-time updates from consumer")

# Hiển thị dữ liệu ban đầu

# Vẽ biểu đồ hình quạt từ cột nhãn của DataFrame ban đầu
st.write("Pie chart of labels:")
label_counts = df['Predicted_Label'].value_counts()
fig, ax = plt.subplots()
ax.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%')
ax.axis('equal')
data_chart = st.pyplot(fig)
top_word_chart = st.pyplot(plot_top_words(df))
st.write("Data:")
data_table = st.table(df.tail(10))
# Tạo một vòng lặp để liên tục cập nhật dữ liệu từ consumer
while True:
    # Đọc file .csv đã được cập nhật
    df_updated = read_csv(csv_file_path)

    # Kiểm tra xem dữ liệu có thay đổi không
    if not df.equals(df_updated):
        # Nếu dữ liệu có thay đổi, cập nhật DataFrame và hiển thị
        df = df_updated
        df=df.dropna()

        label_counts = df['Predicted_Label'].value_counts()

        # Xóa biểu đồ cũ
        data_chart.empty()
        top_word_chart.empty()
        # Vẽ biểu đồ mới
        fig, ax = plt.subplots()
        ax.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%')
        ax.axis('equal')

        # Hiển thị biểu đồ mới
        data_chart = st.pyplot(fig)
        top_word_chart = st.pyplot(plot_top_words(df))
        data_table.table(df.tail(10))
        sleep(20)