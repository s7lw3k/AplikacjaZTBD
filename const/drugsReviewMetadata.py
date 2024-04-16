import pandas as pd


class drugsReviewMetadata:
    all_possible_metadata_options = {
        'ratings': [],
        'drugNames': [],
        'conditions': [],
    }
    selected_metadata_options = all_possible_metadata_options

    def __init__(self):
        df = pd.read_csv('./data/drugsComTest_raw.csv')
        self.all_possible_metadata_options['drugNames'] = df['drugName'].sort_values().unique().tolist()
        self.all_possible_metadata_options['conditions'] = df['condition'].sort_values().unique().tolist()
        self.all_possible_metadata_options['ratings'] = sorted(df['rating'].unique().tolist())
        self.selected_metadata_options = self.all_possible_metadata_options

    def get_all_ratings(self):
        return self.all_possible_metadata_options['ratings']

    def get_all_drug_names(self):
        return self.all_possible_metadata_options['drugNames']

    def get_all_conditions(self):
        return self.all_possible_metadata_options['conditions']

    def get_selected_ratings(self):
        return self.selected_metadata_options['ratings']

    def get_selected_drug_names(self):
        return self.selected_metadata_options['drugNames']

    def get_selected_conditions(self):
        return self.selected_metadata_options['conditions']

    def set_selected_ratings(self, options):
        self.selected_metadata_options['ratings'] = options

    def set_selected_drug_names(self, options):
        self.selected_metadata_options['drugNames'] = options

    def set_selected_conditions(self, options):
        self.selected_metadata_options['conditions'] = options
