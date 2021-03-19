import sys
import clip
import torch
import numpy as np
import pandas as pd
from urllib.request import urlopen
from IPython.display import Image
from IPython.core.display import HTML
import json
from skimage import io

class Unsplash3:
  def __init__(self):
    # Load the open CLIP model
    self.device = "cuda" if torch.cuda.is_available() else "cpu"
    self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
    
    # Load the photo IDs and features vectors
    self.photo_ids = pd.read_csv("unsplash-dataset/photo_ids.csv")
    self.photo_ids = list(self.photo_ids['photo_id'])
    self.photo_features = np.load("unsplash-dataset/features.npy")
    
    # Convert features to Tensors: Float32 on CPU and Float16 on GPU
    if self.device == "cpu":
      self.photo_features = torch.from_numpy(self.photo_features).float().to(self.device)
    else:
      self.photo_features = torch.from_numpy(self.photo_features).to(self.device)

  def encode_search_query(self, search_query):
    with torch.no_grad():
      # Encode and normalize the search query using CLIP
      text_encoded = self.model.encode_text(clip.tokenize(search_query).to(self.device))
      text_encoded /= text_encoded.norm(dim=-1, keepdim=True)
    # Retrieve the feature vector
    return text_encoded

  def find_best_matches(self, text_features):
    # Compute the similarity between the search query and each photo using the Cosine similarity
    similarities = (self.photo_features @ text_features.T).squeeze(1)
    # Sort the photos by their similarity score
    best_photo_idx = (-similarities).argsort()
    # Return the photo IDs of the best matches
    return [self.photo_ids[i] for i in best_photo_idx[:self.results_count]]

  def save_photo(self, photo_id, filename):
    unsplash_api_url = f"https://haltakov.net/unsplash-proxy/{photo_id}"
    photo_data = json.loads(urlopen(unsplash_api_url).read().decode("utf-8"))
    photo_image_url = photo_data["urls"]["raw"] + "&w=320"
    image = io.imread(photo_image_url) 
    io.imsave(fname=filename, arr=image)
    return

  def search_unslash(self, search_query):
    # Encode the search query
    text_features = self.encode_search_query(search_query)
    # Find the best matches
    best_photo_ids = self.find_best_matches(text_features)
    return best_photo_ids

  def run(self, search_query, results_count=3):
    self.results_count = results_count
    best_photo_ids = self.search_unslash(search_query=search_query)
    print(best_photo_ids)
    return best_photo_ids