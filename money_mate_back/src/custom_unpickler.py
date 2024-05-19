import joblib
import pickle

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'EuclideanDistance':
            from sklearn.metrics._dist_metrics import EuclideanDistance
            return EuclideanDistance
        return super().find_class(module, name)

def custom_unpickler(file_path):
    with open(file_path, 'rb') as f:
        return CustomUnpickler(f).load()
