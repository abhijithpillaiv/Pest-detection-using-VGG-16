from skimage import io
from keras.utils import load_img,img_to_array
from keras.models import load_model
import numpy as np
import cv2
import matplotlib.pyplot as plt
from keras.preprocessing import image

img = load_img('../Dataset/test/armyworm/jpg_2.jpg', grayscale=False, target_size=(224, 224))
show_img=load_img('../Dataset/test/armyworm/jpg_2.jpg', grayscale=False, target_size=(224, 224))
disease_class=['aphids','armyworm','beetle','bollworm','grasshopper','mites','mosquito','sawfly','stem_borer']
x = img_to_array(img)
x = np.expand_dims(x, axis = 0)
x /= 255
model=load_model("model.hdf5")
custom = model.predict(x)
print(custom[0])

plt.imshow(show_img)
plt.show()

a=custom[0]
ind=np.argmax(a)
        
print('Prediction:',disease_class[ind])