from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image
import time
from unsplash3 import Unsplash3
from unsplash1 import Unsplash1
from ml import GenerateIdeas
from merge_images import MergeImages
from skimage import io

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
timestr = time.strftime("%Y%m%d-%H%M%S")
image_dir = "/home/arvind/ads/cs329s/static/images"
results_count = 3
model = "notsimple"
# default access page
@app.route("/")
def main():
    return render_template('index.html')

# upload selected image and forward to processing page
@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, image_dir)
    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)
    # retrieve file from html file-picker
    upload = request.files.getlist("file")[0]

    filename = f"input-{timestr}.jpg"
    destination = "/".join([image_dir, filename])
    # If image URL valid, works with image url 
    image_url = request.form["url"]
    if image_url:
        image = io.imread(image_url)
        io.imsave(fname=destination, arr=image)
    else:
        image_name = upload.filename
        ext = os.path.splitext(image_name)[1]
        if (ext == ".jpg") or (ext == ".jpeg") or (ext == ".png") or (ext == ".bmp"):
            print("File accepted")
        else:
            return render_template("error.html", message="Invalid Input"), 400
        upload.save(destination)

    print("File saved to to:", destination)
    # forward to processing page
    return render_template("processing.html", image_name=filename)

# Generate Ad Ideas
@app.route("/ideas", methods=["POST"])
def ideas():
    filename = request.form['image']
    # print(request.form, filename)
    full_filename = "/".join([image_dir, filename]) 
    # Obtain Unsplash suggestions 
    worker = GenerateIdeas(filename=full_filename)
    unsplash_prompts = worker.run()
    # Search unsplash and save each unsplash output photos

    print("\nSearching unsplash....................")
    unsplash_results = []
    splash = None
    if model == "simple":
        splash = Unsplash3() 
        unsplash_prompts = " ".join(unsplash_prompts)
        unsplash_results = splash.run(search_query=unsplash_prompts, results_count=results_count)
    else:
        splash = Unsplash1()
        unsplash_results = splash.run(search_query=unsplash_prompts, results_count=results_count)
    print("\nUnsplash_results:", unsplash_results)
    img_list = []
    for idx, photo_id in enumerate(unsplash_results):
        filename = f"{image_dir}/ideas-{timestr}-{idx}.jpg"
        splash.save_photo(photo_id=photo_id, filename=filename)
        img_list.append(filename)
    print("\nPhotos obtained...merging...")
    # Merge idea images into single image
    outfilename = f"{image_dir}/ideas-{timestr}.jpg"
    merge = MergeImages()
    merge.horizontal(img_list=img_list, save_file=outfilename)
    # Publish merged image to UI
    print("\nSending results to UI...")
    return send_image(f"ideas-{timestr}.jpg")

# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    app.run()

