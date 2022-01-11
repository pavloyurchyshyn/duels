from math import sqrt


class Vector_2d:
    MIN_VALUE = 0.001  # min vector value
    """
    Simple 2D vector.
    """

    def __init__(self, x: float = 0, y: float = 0):
        """
        :param x: float value of vector X value
        :type x: float
        :param y: float value of vector Y value
        :type y: float
        """
        self._x: float = x
        self._y: float = y

    def set(self, x, y):
        self._x, self._y = x, y

    def __iadd__(self, other_vector):
        """
        Add values of another vector to this vector.

        :param other_vector: another vector
        :type other_vector: Vector_2d
        :return: Vector_2d
        """

        self._x += other_vector.x
        self._y += other_vector.y
        return self

    def __isub__(self, other_vector):
        """
        Sub values of another vector from this vector.

        :param other_vector: another vector
        :type other_vector: Vector_2d
        :return: Vector_2d
        """
        self._x -= other_vector.x
        self._y -= other_vector.y
        return self

    def __imul__(self, other_vector):
        """
        Mul vectors

        :type other_vector: Vector_2d
        :return: Vector_2d
        """
        self._x *= other_vector.x
        self._y *= other_vector.y
        return self

    def __len__(self):
        """
        Returns length of vector.

        :return: float
        """
        return sqrt(self._x * self._x + self._y * self._y)

    @property
    def dist(self):
        return sqrt(self._x * self._x + self._y * self._y)

    def mul_k(self, k):
        self._x = k * self._x
        if -Vector_2d.MIN_VALUE < self._x < Vector_2d.MIN_VALUE:
            self._x = 0.0

        self._y = k * self._y
        if -Vector_2d.MIN_VALUE < self._y < Vector_2d.MIN_VALUE:
            self._y = 0.0

        return self

    def reverse(self):
        self._x = -self._x
        self._y = -self._y

        return self

    def add_vector(self, other_vector):
        x, y = self._x, self._y
        self._x += other_vector.x
        self._y += other_vector.y

        other_vector.x += x
        other_vector.y += y
        return self

    def stop(self) -> None:
        self._x = self._y = 0.0
        
        return self

    @property
    def x(self):
        """
        X - x vector value
        :return:
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """
        Y - y vector value
        :return:
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def vector(self) -> tuple:
        """
        Vector values.
        :return:
        """
        return self._x, self._y

    @property
    def negative_vector(self) -> tuple:
        """
        Negative vector values
        :return:
        """
        return -self._x, -self._y

    def __bool__(self) -> bool:
        """
        Boolean value of vector.
        :return:
        """
        return self._x != 0.0 or self._y != 0.0

    def __str__(self):
        return f"{self._x} || {self._y}"
