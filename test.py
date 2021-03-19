from unsplash3 import Unsplash3

splash = Unsplash3()
prompts = splash.run(search_query="a man and a women sitting in restaurant")
print(prompts)