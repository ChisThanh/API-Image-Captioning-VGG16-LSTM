from pickle import load
from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model

def extract_features(filename, model_input):
	model = Model(inputs=model_input.inputs, outputs=model_input.layers[-2].output)
	image = load_img(filename, target_size=(224, 224))
	image = img_to_array(image)
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
	image = preprocess_input(image)
	feature = model.predict(image, verbose=0)
	return feature

def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

def remove_start_end_seq(input_string):
    startseq_length = len("startseq")
    endseq_length = len("endseq")

    if input_string.startswith("startseq") and input_string.endswith("endseq"):
        return input_string[startseq_length:-endseq_length].strip()
    else:
        return input_string


def generate_desc(model, tokenizer, photo, max_length):
	in_text = 'startseq'
	for i in range(max_length):
		sequence = tokenizer.texts_to_sequences([in_text])[0]
		sequence = pad_sequences([sequence], maxlen=max_length)
		yhat = model.predict([photo, sequence], verbose=0)
		yhat = argmax(yhat)
		word = word_for_id(yhat, tokenizer)
		if word is None:
			break
		in_text += ' ' + word
		if word == 'endseq':
			break
		sequence_length = len(in_text.split())
		sequence = pad_sequences([tokenizer.texts_to_sequences([in_text])[0]], maxlen=max_length - sequence_length)
	
	return remove_start_end_seq(in_text)



def load_max_length(max_length=29):
	return max_length

def load_tokenizer(tokenizer_path='tokenizer.pkl'):
    return load(open(tokenizer_path, 'rb'))

def load_caption_model(model_path='model-ep020-loss1.725-val_loss1.328.keras'):
    return load_model(model_path)

def load_and_prepare_photograph(photo_path, model_input):
    return extract_features(photo_path, model_input)

def generate_description(model, tokenizer, photo, max_length):
    return generate_desc(model, tokenizer, photo, max_length)

