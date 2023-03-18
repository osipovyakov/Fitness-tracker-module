from dataclasses import asdict, dataclass


@dataclass
class InfoMessage():
    """Информационное сообщение о тренировке."""
    """"Принимает duration в ч, distance в км, speed в км/ч"""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    text: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        try:
            return self.text.format(**asdict(self))
        except Exception:
            return ('Форматирование не удалось')


class Training:
    """Базовый класс тренировки."""
    """"Принимает duration в ч"""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60

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
        """"Возвращает distance в км"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        """"Возвращает mean_speed в км/ч"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод get_spent_calories не определен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        """"Возвращает duration в ч, distance в км, speed в км/ч"""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    """"Принимает mean_speed в км/ч, duration в ч"""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return ((self.COEFF_CALORIE_1 * mean_speed - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.M_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    """"Принимает mean_speed в км/ч, duration в ч"""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.weight + (self.get_mean_speed()**2
                // self.height) * self.COEFF_CALORIE_2 * self.weight)
                * self.duration * self.M_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    """"Принимает length_pool в м, duration в ч"""
    """Возвращает mean_speed в км/ч"""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: int) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return workouts[workout_type](*data)
    except KeyError:
        return ('Неизвестное действие')
    except Exception:
        return ('Что-то пошло не так')


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
