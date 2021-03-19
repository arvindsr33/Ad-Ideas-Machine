from openai_completion import OpenAICompletion
# from unsplash import Unsplash
# import json
# from urllib.request import urlopen
# from skimage import io
from image_caption import ImageCaption

class GenerateIdeas:
    def __init__(self, filename="/home/arvind/ads/cs329s/test/input_1.jpg", results_count=3):
        self.filename = filename
        self.results_count = results_count
    
    def generate_caption(self, filename):
        # Run image caption 
        ocr = ImageCaption()
        captions = ocr.generate_captions(filename=filename)
        return captions[0]
    
    def openai_ideas(self, description):
        # Generate ideas on caption from openai
        worker = OpenAICompletion()
        result = worker.suggestions(prompt=description)
        while len(result) < self.results_count:
            new_result = worker.suggestions(prompt=description)
            for n in range(len(new_result)):
                result.append(new_result[n])

        prompt = []
        prompt.append(description)
        for i in range(self.results_count):
            prompt.append(result[i])            
        return prompt

    # def search_unsplash(self, prompt):            
        # # Search relevant images on unsplash
        # unsplash_obj = Unsplash()
        # return unsplash_obj.run(search_query=prompt, results_count=self.results_count)

    def run(self):
        caption = self.generate_caption(filename=self.filename)
        print(f"caption: {caption}")
        unsplash_prompt = self.openai_ideas(description=caption)
        print(f"prompt: {unsplash_prompt}")
        # unsplash_results = self.search_unsplash(prompt=unsplash_prompt)
        # print(f"results: {unsplash_results}")
        # return unsplash_results
        return unsplash_prompt

# print(captions)
# description = "two dogs playing in snow"
# results_count=3
# 
# worker = OpenAICompletion()
# result = worker.suggestions(prompt=description)
# while len(result) < results_count:
#     new_result = worker.suggestions(prompt=description)
#     for n in range(len(new_result)):
#         result.append(new_result[n])
# 
# prompt = []
# prompt.append(description)
# for i in range(results_count):
#     prompt.append(result[i])
# unsplash_obj = Unsplash()
# print(prompt)
# 
# unsplash_obj.run(search_query=prompt, results_count=results_count)