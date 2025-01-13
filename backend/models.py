import pandas as pd
from sklearn.tree import DecisionTreeRegressor  # Import DecisionTreeRegressor
import joblib

# Dữ liệu mẫu (giả lập)
data = pd.DataFrame({
    'lap_time': [85, 90, 78, 92, 84, 87],  # Thời gian vòng đua (giây)
    'tire_wear': [0.2, 0.25, 0.15, 0.3, 0.22, 0.18],  # Hao mòn lốp (từ 0 đến 1)
    'race_position': [1, 2, 3, 4, 5, 6],  # Vị trí đua (1 là đầu, 6 là cuối)
    'track_length': [5000, 5000, 5000, 5000, 5000, 5000]  # Độ dài đường đua (mét)
})

X = data[['tire_wear', 'race_position', 'track_length']]  # Các đặc trưng
y = data['lap_time']  # Mục tiêu (thời gian vòng đua)

# Tạo và huấn luyện mô hình Decision Tree Regressor
model = DecisionTreeRegressor()  # Thay thế LinearRegression bằng DecisionTreeRegressor
model.fit(X, y)

# Lưu mô hình đã huấn luyện
joblib.dump(model, 'decision_tree_model.pkl')  # Lưu mô hình cây quyết định
print("Model trained and saved using Decision Tree Regressor.")
