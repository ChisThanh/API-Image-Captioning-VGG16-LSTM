import gdown

url = 'url_vgg16'
output_path = 'vgg16_model.zip'
gdown.download(url, output_path, quiet=False,fuzzy=True)


#pip install gdown