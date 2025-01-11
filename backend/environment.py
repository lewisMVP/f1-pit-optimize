import numpy as np

class F1Environment:
    def __init__(self):
        self.state_size = 4  # [tire_wear, position, track_length, weather]
        self.action_size = 2  # [no_pit, pit]
        self.reset()

    def reset(self):
        self.tire_wear = 1.0
        self.position = np.random.randint(1, 20)
        self.track_length = np.random.uniform(3000, 7000)
        self.weather = np.random.choice([0, 1])  # 0: clear, 1: rain
        return self._get_state()

    def step(self, action):
        # action: 0 = no pit, 1 = pit
        if action == 1:  # pit
            self.tire_wear = 1.0
            self.position = min(20, self.position + 3)  # lose positions during pit
            reward = -25  # pit stop penalty
        else:  # no pit
            self.tire_wear -= 0.1 * (1.2 if self.weather == 1 else 1.0)
            reward = -1 if self.tire_wear > 0.3 else -50  # heavy penalty for worn tires

        done = self.tire_wear <= 0.1
        return self._get_state(), reward, done

    def _get_state(self):
        return np.array([
            self.tire_wear,
            self.position / 20.0,
            self.track_length / 7000.0,
            float(self.weather)
        ])