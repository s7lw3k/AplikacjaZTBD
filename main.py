from PySide6.QtWidgets import QMainWindow, QApplication

from Layout.ChromaWidget import ChromaWidget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.chroma_widget = ChromaWidget(self)
        self.setCentralWidget(self.chroma_widget)


if __name__ == '__main__':
    app = QApplication()

    window = MainWindow()
    window.show()
    app.exec()
