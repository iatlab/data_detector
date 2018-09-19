import os
import pickle
from .spreadsheet import Spreadsheet
from .feature_factory import FeatureFactory

class DataDetector(object):
    """
    Return the probability of being data for a given spreadsheet.

    Possible filetypes are files that can be handled by xlrd: 'xls', 'xlsx', 'csv', etc.

    `DataDetector.detect` returns 1-d array of which dimension corresponds
    to the data probability of each sheet in the spreadsheet.
    """
    DEFAULT_MODEL_FILEPATH      = os.path.join(os.path.dirname(__file__), "model.pkl")
    DEFAULT_VECTORZIER_FILEPATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")
    DEFAULT_SCALER_FILEPATH     = os.path.join(os.path.dirname(__file__), "scaler.pkl")

    def __init__(self, 
                 model_filepath=DEFAULT_MODEL_FILEPATH,
                 vectorizer_filepath=DEFAULT_VECTORZIER_FILEPATH,
                 scaler_filepath=DEFAULT_SCALER_FILEPATH,
                 ):
        with open(model_filepath, "rb") as model_file:
            self.model = pickle.load(model_file)
        with open(vectorizer_filepath, "rb") as vectorizer_file:
            self.vectorizer = pickle.load(vectorizer_file)
        with open(scaler_filepath, "rb") as scaler_file:
            self.scaler = pickle.load(scaler_file)

        model_dim      = len(self.model.feature_importances_)
        vectorizer_dim = len(self.vectorizer.get_feature_names())
        scaler_dim     = len(self.scaler.scale_)
        if model_dim != vectorizer_dim:
            raise ValueError("Dimension Mismatch: "\
                             "the input model expects {} "\
                             "but the vectorizer expects {}"
                             .format(model_dim, vectorizer_dim))
        if model_dim != scaler_dim:
            raise ValueError("Dimension Mismatch: "\
                             "the input model expects {} "\
                             "but the scaler expects {}"
                             .format(model_dim, scaler_dim))

    def detect(self, spreadsheet_filepath):
        """
        Given a spreadsheet filepath,
        return 1-d array of which dimension corresponds to the data probability
        of each sheet in the spreadsheet.
        """
        spreadsheets = Spreadsheet.parse(spreadsheet_filepath)
        features = [FeatureFactory.extract_features(spreadsheet)
                    for spreadsheet in spreadsheets]
        vecs = self.vectorizer.transform(features)
        vecs = self.scaler.transform(vecs)
        probs = self.model.predict_proba(vecs)
        pos_prob = probs[:, 1] # each dim corresponds to 0 and 1.
        return pos_prob
