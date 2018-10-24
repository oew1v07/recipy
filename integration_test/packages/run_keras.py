"""
Sample script that runs sklearn functions logged by recipy.
"""

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
import numpy as np
import keras
import imageio
import joblib

from integration_test.packages.base import Base

from keras import applications, backend, layers, utils

class KerasSample(Base):
    """
    Sample script that runs keras functions logged by recipy.

    This class assumes the existence of a data/keras directory,
    co-located with this file, with the following content:

    * mnist01.jpg
    * mnist02.jpg
    * mnist03.jpg
    * mnist04.jpg
    * mnist05.jpg
    * mnist06.jpg
    * mnist07.jpg
    * mnist08.jpg
    * mnist09.jpg
    * mnist10.jpg
    * mnist.jbl (use X_train, y_train = joblib.load('mnist.jbl'))
    * Model.hdf5


    Running this script with argument 'create_sample_data' will create
    these files.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "keras")

    def datagenerator_flowdirectory(self):
        datagen = keras.preprocessing.image.ImageDataGenerator()

        epochs = 2

        # Only way to test data generator is to flow_from_directory and train
        # simplenet.

        train_generator = datagen.flow_from_directory('data/keras',
                                                      target_size=(28, 28),
                                                      batch_size=32)

    def saveweights(self):
        """ Tests saving out just weights.
        Creates model, loads data into data generator, compiles and fits
        model to generator. Then saves weights.
        """
        datagen = keras.preprocessing.image.ImageDataGenerator()

        epochs = 2

        # Only way to test data generator is to flow_from_directory and train
        # simplenet.

        train_generator = datagen.flow_from_directory('data/keras',
                                                      target_size=(28, 28),
                                                      batch_size=32)

        model = self.SimpleNet()

        fit_dict, compile_dict = self.model_dicts(epochs)

        model.compile(**compile_dict)

        model.fit_generator(train_generator, **fit_dict)

        model.save_weights(os.path.join(self.data_dir, 'Model_Weights.h5'))

    def savemodel(self):
        """ Tests saving out whole model.
        Creates model, loads data into data generator, compiles and fits
        model to generator. Then saves model.
        """
        datagen = keras.preprocessing.image.ImageDataGenerator()

        epochs = 2

        # Only way to test data generator is to flow_from_directory and train
        # simplenet.

        train_generator = datagen.flow_from_directory('data/keras',
                                                      target_size=(28, 28),
                                                      batch_size=32)

        model = self.SimpleNet()

        fit_dict, compile_dict = self.model_dicts(epochs)

        model.compile(**compile_dict)

        model.fit_generator(train_generator, **fit_dict)

        model.save(os.path.join(self.data_dir, 'Whole_Model.h5'))

    def callback_saveweights(self):
        """
        Test saving within a callback works the same as after training.
        """
        datagen = keras.preprocessing.image.ImageDataGenerator()

        epochs = 2

        # Only way to test data generator is to flow_from_directory and train
        # simplenet.

        train_generator = datagen.flow_from_directory('data/keras',
                                                      target_size=(28, 28),
                                                      batch_size=32)

        model = self.SimpleNet()

        fit_dict, compile_dict = self.model_dicts(epochs, checkpoint=True)

        model.compile(**compile_dict)

        model.fit_generator(train_generator, **fit_dict)

    def loadweights(self):
        pass

    def create_sample_image_data(self):
        """
        Create sample data files. The files created are:

            * class5/mnist01.jpg
            * class0/mnist02.jpg
            * class4/mnist03.jpg
            * class1/mnist04.jpg
            * class9/mnist05.jpg
            * class2/mnist06.jpg
            * class1/mnist07.jpg
            * class3/mnist08.jpg
            * class1/mnist09.jpg
            * class4/mnist10.jpg
            * class3/mnist11.jpg
            * class5/mnist12.jpg
            * class3/mnist13.jpg
            * class6/mnist14.jpg
            * class1/mnist15.jpg
            * class7/mnist16.jpg
            * class2/mnist17.jpg
            * class8/mnist18.jpg
            * class6/mnist19.jpg
            * class9/mnist20.jpg
        """
        (X_train, y_train), _ = keras.datasets.mnist.load_data()

        X_train = X_train[:32, :, :]
        y_train = y_train[:32,]

        # Create a list of class folders to create
        classes = np.unique(y_train)

        for cla in classes:
            class_fol = os.path.join(self.data_dir, 'class{}'.format(cla))
            # Check that the folder exists
            if not os.path.exists(class_fol):
                os.makedirs(class_fol)
        
        for i, (x, y) in enumerate(zip(X_train, y_train)):
            img_name = 'mnist{:0>2d}.jpg'.format(i+1)
            fol = os.path.join(self.data_dir, 'class{}'.format(y))
            imageio.imwrite(os.path.join(fol, img_name), x)

        # Create it so the data is in a format to be put into a model        
        # Error with dense layer saying that it was meant to have 10 fields:
        # this means it needs a one-hot-encoding.
        y_train = utils.to_categorical(y_train, num_classes=10)
        X_train = np.expand_dims(X_train, axis=-1)

        joblib.dump((X_train, y_train), os.path.join(self.data_dir, 'mnist.jbl'))

        return (X_train, y_train)

    def create_sample_model(self, training_data, epochs):
        """
        Create sample trained model file. The files created are:

            * Model.h5
        
        This function assumes that the image data to train on has
        been created.
        """
        (X_train, y_train) = training_data

        model = self.SimpleNet()

        fit_dict, compile_dict = self.model_dicts(epochs)

        model.compile(**compile_dict)

        model.fit(X_train, y_train, **fit_dict)

        model.save(os.path.join(self.data_dir, 'Model.h5'))

    def create_sample_data(self):
        epochs = 2
        training_data = self.create_sample_image_data()
        self.create_sample_model(training_data, epochs)
        self.delete_mnist()
    
    def delete_mnist(self):
        """ 
        Deletes the mnist dataset to keep the installation clean.
        Assumes that it is located in "user/.keras/datasets" called
        mnist.npz
        """
        filepath = os.path.join(os.path.expanduser("~"),
                                ".keras",
                                "datasets",
                                "mnist.npz")
        if os.path.exists(filepath)
            os.remove(filepath)


    def model_dicts(self, epochs, checkpoint=False):
        """
        Creates the fit and model dicts with the checkpoint callback if
        necessary.
        """
        fit_dict = {'epochs': epochs,
                    'verbose': 1,
                    'batch_size': 32}
        
        if checkpoint:
            fit_dict['callbacks'] = callbacks.ModelCheckpoint(os.path.join(self.data_dir,
                                                                 'model_{epoch:02d}.hdf5'))

        compile_dict = {'loss': 'categorical_crossentropy',
                        'optimizer': 'sgd',
                        'metrics': ['accuracy']}

        return fit_dict, compile_dict

    def train_checkpoint_epoch_model(self, training_data, epochs):
        pass

    def SimpleNet(self,
                  input_tensor=None,
                  input_shape=(28, 28, 1),
                  weights=None,
                  classes=10):
        """
        Creates a simple convolutional model for the mnist training data.
        This model has one convolutional layer (7, 7) with relu activation,
        a global average pooling layer and a softmax fully-connected layer of
        10 classes.

        Inputs
        ------
        input_tensor: a keras Input instance
        input_shape: tuple (default: (28, 28, 1))
            The sizes of the image dimensions, must include channels=1
            for mnist
        weights: None or path to weights file
        classes: int
            The number of classes to be represented in the softmax

        """  
        input_shape = applications.imagenet_utils._obtain_input_shape(input_shape,
                                          default_size=28,
                                          min_size=14,
                                          data_format=backend.image_data_format(),
                                          require_flatten=True,
                                          weights=weights)

        if input_tensor is None:
            img_input = layers.Input(shape=input_shape)
        else:
            if not backend.is_keras_tensor(input_tensor):
                img_input = layers.Input(tensor=input_tensor, shape=input_shape)
            else:
                img_input = input_tensor

        x = layers.ZeroPadding2D(padding=((3, 3), (3, 3)))(img_input)
        x = layers.Conv2D(32, 7, strides=2, use_bias=False, name='conv1/conv')(x)
        x = layers.Activation('relu', name='conv1/relu')(x)
        x = layers.Flatten()(x)
        x = layers.Dense(classes, activation='softmax', name='fc10')(x)

        # Ensure that the model takes into account
        # any potential predecessors of `input_tensor`.
        if input_tensor is not None:
            if hasattr(keras.utils, 'get_source_inputs'):
                get_source_inputs = keras.utils.get_source_inputs
            else:
                from keras import engine
                get_source_inputs = engine.get_source_inputs
            inputs = get_source_inputs(input_tensor)
        else:
            inputs = img_input

        model = keras.Model(inputs, x, name='simplenet')

        if weights is not None:
            model.load_weights(weights)
    
        return model


if __name__ == "__main__":
    KerasSample().invoke(sys.argv)
