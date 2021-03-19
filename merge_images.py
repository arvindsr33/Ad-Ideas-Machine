import numpy as np
import PIL
from PIL import Image

class MergeImages:
    def __init__(self):
        pass
    def horizontal(self, img_list, save_file):
        imgs    = [ PIL.Image.open(i) for i in img_list]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

        # save that beautiful picture
        imgs_comb = PIL.Image.fromarray( imgs_comb)
        imgs_comb.save(save_file)    
        return

    def vertical(self, img_list, save_file):
        imgs    = [ PIL.Image.open(i) for i in img_list]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

        # for a vertical stacking it is simple: use vstack
        imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        imgs_comb = PIL.Image.fromarray( imgs_comb)
        imgs_comb.save(save_file)
        return 