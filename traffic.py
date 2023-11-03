import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Constants
EPOCHS = 10
IMG_WIDTH, IMG_HEIGHT = 30, 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

def load_data(data_dir):
    images = []
    labels = []

    for directory in os.listdir(data_dir):
        print(f"Loading files from {directory} directory...")
        label = int(directory)
        for file in os.listdir(os.path.join(data_dir, directory)):
            image = cv2.imread(os.path.join(data_dir, directory, file))
            resized_image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
            images.append(resized_image)
            labels.append(label)
        print(f"Finished loading files from {directory} directory.")

    return images, labels

def get_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=input_shape),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()
    return model

def main():
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    images, labels = load_data(sys.argv[1)
    labels = tf.keras.utils.to_categorical(labels)

    x_train, x_test, y_train, y_test = train_test_split(np.array(images) / 255.0, np.array(labels), test_size=TEST_SIZE)

    model = get_model(input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
    model.fit(x_train, y_train, epochs=EPOCHS)

    loss, accuracy = model.evaluate(x_test, y_test, verbose=2)
    print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy:.4f}")

    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")

if __name__ == "__main__":
    main()
