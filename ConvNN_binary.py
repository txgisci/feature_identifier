import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  #filters out tensorflow INFO logs, but keeps WARNING and ERROR logs
import keras
import matplotlib.pylab as plt
import time
import tensorflow as tf
from keras.utils import multi_gpu_model
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense, AveragePooling2D
from keras import backend as K
from keras.callbacks import Callback, ModelCheckpoint

#Training parameters
#nb_epoch = 128
#for d in ['/device:GPU:1']:
#	with tf.device(d):
nb_epoch = 128
#nb_train_samples = 8
#nb_test_samples = 2
#batch_size = 2  
nb_train_samples = 1500
nb_test_samples = 250
batch_size = 128  #This is how many images are processed at once (before weights are adjusted).  Make this number smaller if you run out of GPU memory.

# dimensions of our images.
img_width, img_height = 336, 224

#filename that model will be saved with:
saved_model_filename_no_ext='model-Limb-'+str(img_width)+'x'+str(img_height)+'-shape=32-32-64-64--'+str(nb_train_samples)+'-samples-'+str(nb_epoch)+'-epochs'
saved_model_filename=saved_model_filename_no_ext+'.h5'
#filepath if saving at checkpoints is enabled:
checkpoint_filepath='trained_network_models//checkpoints//save_every_epoch//'+saved_model_filename_no_ext+'-epoch={epoch:03d}-val_acc={val_acc:.3f}-loss={loss:.3f}-val_loss={val_loss:.3f}.h5'

#image_dir = 'E:\\MarkLambertImages\\'
#image_dir = 'C:\\Users\\mdlambe1\\Pictures\\Earthlimb_pics_336x224'
#image_dir = 'C:\\Users\\Aaron\\Desktop\\GEO_ML\\island'
image_dir = '//home//aaron//projectDir//island_images_336x224'

train_data_dir = image_dir + '//train'
test_data_dir = image_dir + '//test'

start_time=time.time()

class AccuracyHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.acc = []
        self.loss = []
        self.val_acc = []
        self.val_loss = []

    def on_epoch_end(self, epoch, logs={}):
        self.acc.append(logs.get('acc'))
        self.loss.append(logs.get('loss'))
        self.val_acc.append(logs.get('val_acc'))
        self.val_loss.append(logs.get('val_loss'))
		
history = AccuracyHistory()

#defines how images should be augmented
datagen = ImageDataGenerator(rescale=1./255, # used to rescale the pixel values from [0, 255] to [0, 1] interval.  This normalizes the data
        #shear_range=0.2,       # randomly applies shearing transformation
        #zoom_range=0.2,        # randomly applies zoom transformation - Zoom may cut off small clouds from edge of image, making a cloud image into a no_cloud image
		#rotation_range=10,	    # randomly rotates image (in degrees)
		#samplewise_center=True, # centers dataset by subtracting mean image.
        horizontal_flip=True,   # randomly flip the images 
        vertical_flip=True) 
		
# automagically retrieve images and their classes randomly for train and validation sets
train_generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary')

test_generator = datagen.flow_from_directory(
        test_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary')

# Architecture of NN
#for d in ['/device:GPU:1']:
with tf.device("/cpu:0"):
	model = Sequential()
	model.add(Conv2D(32,(3, 3), input_shape=(img_height, img_width, 3),padding='same',kernel_initializer='lecun_normal'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(32,(3, 3),padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(64,(3, 3),padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(64,(3, 3),padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(AveragePooling2D(pool_size=(2,2)))
	model.add(Flatten())
	'''model.add(Dense(1024))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(1024))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))'''
	model.add(Dense(1))
	model.add(Activation('sigmoid'))

#making model parallel for gpu
model = multi_gpu_model(model, gpus=4)

my_rmsprop = keras.optimizers.RMSprop(lr=0.0001, rho=0.9, epsilon=1e-07, decay=0.0)
model.compile(loss='binary_crossentropy',
              optimizer=my_rmsprop,
              metrics=['accuracy'])

# checkpoint (to save model after every epoch).  Need to call checkpoint as a callback in model.fit_generator for this to work.
checkpoint = ModelCheckpoint(checkpoint_filepath, verbose=1, save_best_only=False)

#save only if validation accuracy improves:
#filepath='trained_network_models//checkpoints//save_every_epoch//'+saved_model_filename
#checkpoint = ModelCheckpoint(checkpoint_filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')

model.fit_generator(
        train_generator,
        steps_per_epoch=nb_train_samples/batch_size,
        epochs=nb_epoch,
        verbose=1,
        validation_data=test_generator,
        validation_steps=nb_test_samples/batch_size,
		callbacks=[history, checkpoint])
		#callbacks=[history])
		
#Save final model to HDF5



model.save('trained_network_models//'+saved_model_filename)

# Evaluating on the testing set
#model.evaluate_generator(test_generator, nb_test_samples)

# Calculate runtime
time_in_seconds=time.time() - start_time
hours = time_in_seconds // 3600
minutes = time_in_seconds % 3600 // 60
seconds = time_in_seconds % 60
print('total runtime: ', hours, ' hours, ', minutes, ' minutes, and ', seconds, ' seconds') 

# Plot accuracy
#plt.figure(0)
plt.plot(range(0, nb_epoch), history.acc)
plt.plot(range(0, nb_epoch), history.val_acc)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('trained_network_models//plots//'+saved_model_filename+'.png')
plt.close()

plt.figure(1)
plt.plot(range(0, nb_epoch), history.loss)
plt.plot(range(0, nb_epoch), history.val_loss)
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.savefig('trained_network_models//plots//loss//'+saved_model_filename+'.png')
plt.close()
