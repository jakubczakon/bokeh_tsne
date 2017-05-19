import pandas as pd

from sklearn.manifold import TSNE

from utils import *
from hover_scatter import scatterplot


class TsneVis():
    def __init__(self, model, feature_layer_name, **tsne_kwargs):
        self.tsne_model_ = TSNE(**tsne_kwargs)
        self.model_ = model
        self.feature_layer_name_ = feature_layer_name
        
        self.tsne_features_ = None
    
    def plot(self, **kwargs):
        scatterplot(self.tsne_features_, **kwargs)
    
    def fit(self, img_folder, batch_size=2):
        img_input_shape = self.model_.input_shape[1:-1]
        img_paths, img_tensor = folder2tensor(img_folder, paths=True, shape=None)
        img_features = self._extract_features(img_tensor, batch_size)
        
        tsne_features = self.tsne_model_.fit_transform(img_features)
        
        df = pd.DataFrame(tsne_features, columns=['x','y'])
        df['img_filepath'] = img_paths
        self.tsne_features_ = df
        
    def _extract_features(self,X, batch_size):
        layer_id = [i for i, l in enumerate(self.model_.layers) 
                    if l.name == self.feature_layer_name_][0]
        img_features = get_layer_output(self.model_, 
                                        layer=layer_id, X=X, batch_size=batch_size)

        new_shape = np.product(img_features.shape[1:])
        nr_imgs = img_features.shape[0]
        img_features = np.reshape(img_features,(nr_imgs, new_shape))
        return img_features