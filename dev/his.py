import numpy as np
import matplotlib.pyplot as plt

# Khởi tạo danh sách rỗng để lưu các số
data = []

# Số lượng bin
num_bins = 10

# Giả sử chúng ta có các số được cấp dần qua mỗi vòng lặp
new_values = [2, 5, 1, 7, 8, 12, 9, 15, 3, 6, 4, 10]  # Thay đổi tuỳ ý

# Vòng lặp để tính histogram tích lũy
for i, val in enumerate(new_values):
    data.append(val)  # Thêm giá trị mới vào danh sách

    # Cập nhật min và max giá trị trong danh sách hiện tại
    min_value = min(data)
    max_value = max(data)

    # Cập nhật khoảng bin từ min đến max hiện tại
    bins = np.linspace(min_value, max_value, num_bins + 1)

    # Tính histogram tích lũy
    hist, _ = np.histogram(data, bins=bins)

    # Hiển thị kết quả sau mỗi vòng lặp
    print(f"Histogram sau vòng lặp {i+1}: {hist}")

    # Nếu muốn hiển thị biểu đồ có thể dùng matplotlib
    plt.hist(data, bins=bins, edgecolor="black", alpha=0.7)
    plt.title(f"Histogram sau {i+1} vòng lặp")
    plt.xlabel("Giá trị")
    plt.ylabel("Tần suất")
    plt.show()
