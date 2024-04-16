from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider


def makeSlider(min: int, max: int, value: int) -> QSlider:
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min)
    slider.setMaximum(max)
    slider.setValue(value)
    return slider