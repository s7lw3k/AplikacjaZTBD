from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog, QFormLayout, QLabel, QListView, QDialogButtonBox


class MetadataDialog(QDialog):
    def __init__(self,  title, message, items, parent=None):
        super(MetadataDialog, self).__init__(parent=parent)
        form = QFormLayout(self)
        form.addRow(QLabel(message))
        self.listView = QListView(self)
        form.addRow(self.listView)
        model = QStandardItemModel(self.listView)
        self.setWindowTitle(title)
        for item in items:
            standard_item = QStandardItem(item[0])
            standard_item.setCheckState(Qt.Checked if item[1] else Qt.Unchecked)
            standard_item.setCheckable(True)
            standard_item.setEditable(False)
            model.appendRow(standard_item)
        self.listView.setModel(model)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        form.addRow(button_box)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def itemsSelected(self):
        selected = []
        model = self.listView.model()
        i = 0
        while model.item(i):
            if model.item(i).checkState() == Qt.Checked:
                selected.append(model.item(i).text())
            i += 1
        return selected