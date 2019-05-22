 # Convolutional Neural Network

import pickle
from pathlib import Path

# import plaidml.keras

# import tensorflow as tf

# plaidml.keras.install_backend()

import os

os.environ['MKL_THREADING_LAYER'] = 'GNU'
os.environ['THEANO_FLAGS'] = 'blas.ldflags=-lblas'
os.environ['KERAS_BACKEND'] = 'theano'
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["KMP_BLOCKTIME"] = "30"
os.environ["KMP_SETTINGS"] = "1"
os.environ["KMP_AFFINITY"]= "granularity=fine,verbose,compact,1,0"#:w

# Importing the Keras libraries and packages
import keras.models as km
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras import losses as kl
from keras import optimizers as ko
from keras import backend as K

# Initialising the CNN
input_size = ( 128, 128 )
spe = 8000.
epochCount = 90

def createModel(): 

    classifier = Sequential()
    classifier.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(*input_size,3)))
    classifier.add(MaxPooling2D((2, 2)))
    classifier.add(Dropout(0.25))

    classifier.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Dropout(0.25))

    classifier.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    classifier.add(Dropout(0.4))

    classifier.add(Flatten())

    classifier.add(Dense(128, activation='relu'))
    classifier.add(Dropout(0.3))
    classifier.add(Dense(4, activation='softmax'))

    classifier.compile(loss=kl.categorical_crossentropy,
                       optimizer=ko.Adam(),
                       metrics=['accuracy']
                      )

    return classifier

import numpy as np

def load(filename):

    from PIL import Image
    from skimage import transform
    import matplotlib.pyplot as plt

    np_image = Image.open(filename)
    np_image = np_image.resize( ( 128, 128 ) )

    # plt.imshow( np_image )
    # plt.show()
    np_image = np.array(np_image).astype('float32')/255.
    np_image = np.reshape( np_image, [ 1, 128, 128, 3 ] )
    # np_image = np.expand_dims(np_image, axis=0)

    return np_image

def predict( predictor, filename ): 

    from keras.preprocessing import image
    from keras.applications.resnet50 import preprocess_input

    filePath = Path( filename ) 
    
    if filePath.is_file():

        image = load( filename )
        result = predictor.predict_classes( image )
        # print( result ) 

        prediction = ""

        if result[0] == 0:
            prediction = 'bird'
        elif result[0] == 1:
            prediction = 'cat'
        elif result[0] == 2:
            prediction = 'dog'
        else:
            prediction = 'other'

        return prediction
        
        # print( filename  + '\t' + prediction + '\t' ) 

def createPredictions( predictor ): 

    import glob

    for filepath in glob.iglob('/media/elliott/Archive1/AITestData/dataset/training_set/cats/*.jpg'):
        predict( predictor, filepath )

    # for filepath in glob.iglob('tests/*.jpg'):
        # predict( predictor, filepath )

def createOldPredictions( predictor ): 

    for img in range( 10,101 ):
        
        filename = '/media/elliott/Archive1/AITestData/256_ObjectCategories/089.goose/089_00' + str( img ) + '.jpg'

        predict( predictor, filename )

# config = tf.ConfigProto(intra_op_parallelism_threads=int(8), inter_op_parallelism_threads=2, allow_soft_placement=True, device_count = {'CPU': int(8)})

# session = tf.Session(config=config)

# K.set_session(session)            

modelFile   = 'birds.test.model'
weightsFile = 'weights.test.model'

modelPath = Path( modelFile )

from keras.preprocessing.image import ImageDataGenerator

classifier = createModel()
    
if not modelPath.is_file():
    
    batch_size = 32
    
    # Part 2 - Fitting the CNN to the images    
    train_datagen = ImageDataGenerator( rescale         = 1./255,
                                        shear_range     = 0.2,
                                        zoom_range      = 0.2,
                                        horizontal_flip = True
                                       )

    test_datagen = ImageDataGenerator( rescale = 1./255 )
    
    training_set = train_datagen.flow_from_directory('/media/elliott/Archive1/AITestData/dataset/training_set/',
                                                target_size = input_size,
                                                batch_size = batch_size,
                                                class_mode = 'categorical')
    
    test_set = test_datagen.flow_from_directory('/media/elliott/Archive1/AITestData/dataset/test_set/',
                                                target_size = input_size,
                                                batch_size = batch_size,
                                                class_mode = 'categorical')
    
    classifier.fit_generator(training_set,
                             steps_per_epoch     = spe / batch_size,
                             epochs              = epochCount,
                             validation_data     = test_set,
                             validation_steps    = spe / ( batch_size * 4. ),
                             workers             = 10,
                             max_q_size          = 100,
                             use_multiprocessing = True,
                             shuffle             = True
                             )

    print( "Model class indices: ", training_set.class_indices )
    print( "Test class indices: ", test_set.class_indices )

    weights = classifier.get_weights();
        
    with open( weightsFile, 'wb' ) as output:
        pickle.dump( weights, output, pickle.HIGHEST_PROTOCOL )
        
    classifier.save( modelFile )

    classifier.summary()

    createPredictions( classifier )

else:

    from keras.models import load_model
    from camera3 import checkCamera
    import matplotlib.pyplot as plt

    classifier = load_model( modelFile )
        
    while True:

        np_image = checkCamera()

        classified = predict( classifier, './c1.jpg' )

        print( classified )

        if classified == "cat": 
            plt.imshow( np_image )
            plt.show()

    # with open( weightsFile, 'rb' ) as input:
         # weights = pickle.load( input )
         # classifier.set_weights( weights )


