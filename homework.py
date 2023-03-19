class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = "%.3f" % float(duration)
        self.distance = "%.3f" % float(distance)
        self.speed = "%.3f" % float(speed)
        self.calories = "%.3f" % float(calories)

    def get_message(self):
        message = f"Тип тренировки: {self.training_type}; Длительность: {self.duration} ч.;" \
                  f" Дистанция: {self.distance} км; Ср. скорость: {self.speed} км/ч; Потрачено ккал: {self.calories}."
        return message


class Training:
    """Базовый класс тренировки."""
    __dict__ = {'LEN_STEP': 0.65,
                'M_IN_KM': 1000}
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(calories=self.get_spent_calories(), distance=self.get_distance(),
                           speed=self.get_mean_speed(), duration=self.duration,
                           training_type=self.__class__.__name__.__str__())
        return info


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)
        self.coeff_calorie1 = 18
        self.coeff_calorie2 = 20

    def get_spent_calories(self) -> float:
        calories = (self.coeff_calorie1 * self.get_mean_speed() - self.coeff_calorie2) * self.weight / self.M_IN_KM * (
                self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: float, weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height
        self.coeff_calorie1 = 0.035
        self.coeff_calorie2 = 2
        self.coeff_calorie3 = 0.029

    def get_spent_calories(self) -> float:
        calories = (self.coeff_calorie1 * self.weight + (
                self.get_mean_speed() ** self.coeff_calorie2 // self.height) * self.coeff_calorie3 * self.weight) * (
                           self.duration * 60)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return calories

    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict1 = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training1 = dict1.get(workout_type)(*data)
    return training1


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
