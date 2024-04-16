import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout, QDialog

import chromadb

from Dialogs.metadataDialog import MetadataDialog
from Helpers.layout import makeSlider
from const.drugsReviewMetadata import drugsReviewMetadata

client = chromadb.HttpClient(host='localhost', port=8000)


def getChromaCollection():
    return client.get_or_create_collection(name="DrugsReviews")


def removeAndGetChromaCollection():
    client.delete_collection(name="DrugsReviews")
    return client.get_or_create_collection(name="DrugsReviews")


class ChromaWidget(QWidget):
    queryText = ''
    new_rec_quantity = 100
    respond_quantity = 5

    all_options = ['sadness', 'joy', 'love', 'anger', 'fear', 'suprise']
    selected_options = all_options

    def showRes(self) -> None:
        out_values = self.collection.query(query_texts=self.queryText,
                                           n_results=self.respond_quantity)
        out_text = ''
        for i in range(self.respond_quantity):
            out_text += f'({i + 1}) Recenzja: {out_values['documents'][0][i]}\n'
            out_text += f'Odległóść: {out_values['distances'][0][i]}\n'
            out_text += f'Metadane: {out_values['metadatas'][0][i]}\n\n'
        self.output_label.setText(f"{out_text}")

    def set_queryText(self, val):
        self.queryText = val

    def set_new_rec_quantity(self, val):
        self.new_rec_quantity = val
        self.input_range_label.setText(f'Ilość nowych rekordów ({self.new_rec_quantity})')

    def set_new_respond_quantity(self, val):
        self.respond_quantity = val
        self.respond_quantity_label.setText(f'Liczba wyników ({self.respond_quantity})')

    def clear_rec(self):
        self.collection = removeAndGetChromaCollection()
        self.clear_label.setText(f'Wyczyść wszystkie: ({self.collection.count()}) rekordów')

    def show_metadata_dialog(self):
        items = []
        for option in self.drugsMetadataHandler.get_all_drug_names():
            items.append([option, option in self.drugsMetadataHandler.get_selected_drug_names()])
        dial = MetadataDialog("Możliwe leki", "Lista możliwych emocji", items, self)
        if dial.exec_() == QDialog.Accepted:
            self.drugsMetadataHandler.set_selected_drug_names(dial.itemsSelected())

    def insert_new_rec(self):
        import pandas as pd
        df = pd.read_csv('./data/drugsComTest_raw.csv', sep=',', skiprows=self.collection.count() + 1,
                         nrows=self.new_rec_quantity)
        drug_name = df.iloc[:, 1].tolist()
        condition = df.iloc[:, 2].tolist()
        docs = df.iloc[:, 3].tolist()
        rating = df.iloc[:, 4].tolist()
        metadata = [{'source': './drugsComTest_raw.csv',
                     'drugName': drug_name[i],
                     'condition': condition[i],
                     'rating': rating[i]} for i in range(len(rating))]
        ids = [str(x) for x in df.iloc[:, 0].to_list()]
        start_time = time.perf_counter()
        self.collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )
        end_time = time.perf_counter()
        self.input_range_label.setText(
            f'Ilość nowych rekordów ({self.new_rec_quantity}) \nCzas: ' + f'{end_time - start_time:0.4f}' + ' sekund')
        self.clear_label.setText(f'Wyczyść wszystkie: ({self.collection.count()}) rekordów')

    def __init__(self, parent):
        super(ChromaWidget, self).__init__(parent)
        layout_items = []

        itle_label = QLabel(f'Chroma')
        layout_items.append(itle_label)

        self.collection = getChromaCollection()

        self.drugsMetadataHandler = drugsReviewMetadata()

        # NEW DATA
        self.input_range_label = QLabel(f'Ilość nowych rekordów ({self.new_rec_quantity})')
        layout_items.append(self.input_range_label)

        new_data_layout = QHBoxLayout()
        new_data_layout.setContentsMargins(0, 0, 0, 0)
        population_size_slider = makeSlider(10, 10000, self.new_rec_quantity)
        population_size_slider.valueChanged.connect(self.set_new_rec_quantity)
        new_data_layout.addWidget(population_size_slider)

        insert_button = QPushButton('Wstaw nowe rekordy')
        insert_button.clicked.connect(self.insert_new_rec)
        new_data_layout.addWidget(insert_button)

        new_data_container = QWidget(self)
        new_data_container.setLayout(new_data_layout)
        layout_items.append(new_data_container)

        # CLEAR DB
        clear_layout = QHBoxLayout()
        clear_layout.setContentsMargins(0, 0, 0, 0)
        self.clear_label = QLabel(f'Wyczyść wszystkie: ({self.collection.count()}) rekordów')
        clear_layout.addWidget(self.clear_label)

        clear_button = QPushButton('Wyczyść')
        clear_button.clicked.connect(self.clear_rec)
        clear_layout.addWidget(clear_button)

        clear_container = QWidget()
        clear_container.setLayout(clear_layout)
        layout_items.append(clear_container)

        # QUERY
        query_layout = QHBoxLayout()
        query_layout.setContentsMargins(0, 0, 0, 0)
        input_label = QLabel('Podaj zapytanie do bazy')
        query_layout.addWidget(input_label)

        input_button = QPushButton('Wyśli zapytanie')
        input_button.clicked.connect(self.showRes)
        query_layout.addWidget(input_button)

        query_container = QWidget()
        query_container.setLayout(query_layout)
        layout_items.append(query_container)

        text_input = QLineEdit(self)
        text_input.textChanged.connect(self.set_queryText)
        layout_items.append(text_input)

        # Metadata dialog
        metadata_button = QPushButton('Wybierz wymagane cechy')
        metadata_button.clicked.connect(self.show_metadata_dialog)
        query_layout.addWidget(metadata_button)

        # Respond Quantity
        self.respond_quantity_label = QLabel(f'Liczba wyników ({self.respond_quantity})')
        layout_items.append(self.respond_quantity_label)
        respond_quantity_slider = makeSlider(1, 1000, self.respond_quantity)
        respond_quantity_slider.valueChanged.connect(self.set_new_respond_quantity)
        layout_items.append(respond_quantity_slider)

        self.output_label = QLabel('')
        # self.output_label.setMaximumWidth(200)
        scrollArea = QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.output_label)
        layout_items.append(scrollArea)

        self.layout = QVBoxLayout()
        for item in layout_items:
            self.layout.addWidget(item)
        self.setLayout(self.layout)
