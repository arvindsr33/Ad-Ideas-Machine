from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

class ImageCaption:
    def __init__(self):
        subscription_key = # Your subscription key here
        endpoint = # Your endpoint here
        self.computervision_client = ComputerVisionClient(
            endpoint, CognitiveServicesCredentials(subscription_key)
        )

    def generate_captions(self, filename="/home/arvind/ads/cs329s/images/image_0.jpg"):
        stream = open(filename, "rb")

        """ Describe an Image with confidence score """
        # description_results = computervision_client.describe_image(remote_image_url) # API Call
        description_results = self.computervision_client.describe_image_in_stream(stream)
        # print(description_results)

        # Get the captions (descriptions) from the response, with confidence level
        captions = []
        print("\nDescription of remote image: ")
        if len(description_results.captions) == 0:
            print("No description detected.")
        else:
            for caption in description_results.captions:
                captions.append(caption.text)
                print(
                    "'{}' with confidence {:.2f}%".format(
                        caption.text, caption.confidence * 100)
                )
        return captions