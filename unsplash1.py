import sys
import clip
import torch
import numpy as np
import pandas as pd
from urllib.request import urlopen
#from IPython.display import Image
#from IPython.core.display import HTML
import json
from skimage import io

class Unsplash1:
  def __init__(self):
    # Load the open CLIP model
    self.device = "cuda" if torch.cuda.is_available() else "cpu"
    self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    # Load the photo IDs and features vectors
    self.photo_ids = pd.read_csv("/home/arvind/ads/cs329s/unsplash-dataset/photo_ids.csv")
    self.photo_ids = list(self.photo_ids['photo_id'])
    self.photo_features = np.load("/home/arvind/ads/cs329s/unsplash-dataset/features.npy")

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
    return self.photo_ids[best_photo_idx[0]]

  def save_photo(self, photo_id, filename):
    # Proxy for the Unsplash API so that I don't expose my access key
    unsplash_api_url = f"https://haltakov.net/unsplash-proxy/{photo_id}"
    photo_data = json.loads(urlopen(unsplash_api_url).read().decode("utf-8"))

    # Get the URL of the photo resized to have a width of 480px
    photo_image_url = photo_data["urls"]["raw"] + "&w=320"

    # Display the photo
    # display(Image(url=photo_image_url))
    image = io.imread(photo_image_url) 
    # print(f"Image saved to {filename}")
    io.imsave(fname=filename, arr=image)

  def search_unslash(self, search_query):
    # Encode the search query
    text_features = self.encode_search_query(search_query)
    # Find the best matches
    best_photo_ids = self.find_best_matches(text_features)
    # print(f"Best photo ids: {best_photo_ids}")
    return best_photo_ids

  def run(self, search_query, results_count=3):
    self.results_count = results_count
    best_photo_ids = set() 
    count = 0
    while count < results_count:
      query = " ".join([search_query[0], search_query[count+1]])
      photo_id = self.search_unslash(query)
      best_photo_ids.add(photo_id)
      count += 1
    return list(best_photo_ids)