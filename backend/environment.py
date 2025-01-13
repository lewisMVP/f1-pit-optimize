# environment.py
import numpy as np

class RaceEnvironment:
    def __init__(self, track_conditions, initial_tire_health=1.0, weather="clear"):
        self.track_conditions = track_conditions  # Các đặc điểm của đường đua
        self.tire_health = initial_tire_health  # Khởi tạo độ hao mòn lốp (1 là mới)
        self.weather = weather
        self.position = 1  # Vị trí xuất phát
        self.lap_time = 0
        self.current_lap = 1
        self.max_laps = 50  # Tổng số vòng đua
        self.done = False

    def step(self, action):
        """
        Hàm mô phỏng một bước đua.
        action = 1 (pit stop), 0 (không pit stop)
        """
        if action == 1:  # Nếu chọn pit stop
            self.tire_health = 1.0
            self.lap_time += 25  # Giả định mất 25 giây cho pit stop
        else:
            # Hao mòn lốp theo điều kiện đường đua và thời tiết
            self.tire_health -= self.track_conditions['wear_rate'] * (1.1 if self.weather == "rain" else 1.0)
            self.lap_time += self.track_conditions['base_time'] * (1 / self.tire_health)
        
        self.current_lap += 1
        self.done = self.current_lap >= self.max_laps
        reward = -self.lap_time  # Khuyến khích giảm thời gian

        return (self.position, self.tire_health, self.current_lap), reward, self.done

    def reset(self):
        self.tire_health = 1.0
        self.position = 1
        self.lap_time = 0
        self.current_lap = 1
        self.done = False
        return (self.position, self.tire_health, self.current_lap)
