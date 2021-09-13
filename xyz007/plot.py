import mp520 as mp
import time
import sys
import os
import random

import matplotlib.pyplot as plt

DATA_WIDTH = 28
DATA_HEIGHT = 28
NUMBER_OF_TRAINING_EXAMPLES = 5000
NUMBER_OF_VALIDATION_EXAMPLES = 1000

ALL_TRAINING_IMAGES = []
ALL_TRAINING_LABELS = []
ALL_VALIDATION_IMAGES = []
ALL_VALIDATION_LABELS = []

"""
Convert ASC-II pixel into numerical data and vise versa

    - ' ' is converted to 0, which means it's part of the background
    - '#' is converted to 1, part of the image interior
    - '+' is converted to 2, part of the image exterios (i.e., edges)
    
"""


def _pixel_to_value(character):
    if character == " ":
        return 0
    elif character == "#":
        return 1
    elif character == "+":
        return 2


def _value_to_pixel(value):
    if value == 0:
        return " "
    elif value == 1:
        return "#"
    elif value == 2:
        return "+"


"""
Function for loading data and label files
"""


def _load_data_file(filename, n, width, height):
    fin = [l[:-1] for l in open(filename).readlines()]
    fin.reverse()
    items = []
    for i in range(n):
        data = []
        for j in range(height):
            row = list(map(_pixel_to_value, list(fin.pop())))
            data.append(row)
        items.append(data)
    return items


def _load_label_file(filename, n):
    fin = [l[:-1] for l in open(filename).readlines()]
    labels = []
    for i in range(n):
        labels.append(int(fin[i]))
    return labels


"""
Helper function for prting an image
"""


def _print_digit_image(data):
    for row in range(len(data)):
        print("".join(map(_value_to_pixel, data[row])))


"""
Loading all data into a list of "pixels" with some edge information
"""


def _load_all_data():
    global ALL_TRAINING_IMAGES
    global ALL_TRAINING_LABELS
    global ALL_VALIDATION_IMAGES
    global ALL_VALIDATION_LABELS

    ALL_TRAINING_IMAGES = _load_data_file(
        "digitdata/trainingimages", NUMBER_OF_TRAINING_EXAMPLES, DATA_WIDTH, DATA_HEIGHT
    )
    ALL_TRAINING_LABELS = _load_label_file(
        "digitdata/traininglabels", NUMBER_OF_TRAINING_EXAMPLES
    )

    ALL_VALIDATION_IMAGES = _load_data_file(
        "digitdata/validationimages",
        NUMBER_OF_VALIDATION_EXAMPLES,
        DATA_WIDTH,
        DATA_HEIGHT,
    )
    ALL_VALIDATION_LABELS = _load_label_file(
        "digitdata/validationlabels", NUMBER_OF_VALIDATION_EXAMPLES
    )


if __name__ == "__main__":

    # Load all data
    _load_all_data()

    def train_and_report_accuracy(
        data_width,
        data_height,
        training_images,
        training_labels,
        testing_images,
        testing_labels,
        feature_extractor,
        training_percentage,
    ):
        # Train
        mp.compute_statistics(
            training_images,
            training_labels,
            data_width,
            data_height,
            feature_extractor,
            training_percentage,
        )
        # Inference
        predicted_labels = mp.classify(
            testing_images, data_width, data_height, feature_extractor
        )
        #
        correct_count = 0.0
        for ei in range(len(predicted_labels)):
            if testing_labels[ei] == predicted_labels[ei]:
                correct_count += 1
        return correct_count / len(predicted_labels)

    percentages = range(10, 101, 10)

    # Get the accuracy when using basic features
    basic_accuracy = [
        train_and_report_accuracy(
            DATA_WIDTH,
            DATA_HEIGHT,
            ALL_TRAINING_IMAGES,
            ALL_TRAINING_LABELS,
            ALL_VALIDATION_IMAGES,
            ALL_VALIDATION_LABELS,
            mp.extract_basic_features,
            p,
        )
        for p in percentages
    ]
    # Get the accuracy when using advanced features
    advanced_accuracy = [
        train_and_report_accuracy(
            DATA_WIDTH,
            DATA_HEIGHT,
            ALL_TRAINING_IMAGES,
            ALL_TRAINING_LABELS,
            ALL_VALIDATION_IMAGES,
            ALL_VALIDATION_LABELS,
            mp.extract_advanced_features,
            p,
        )
        for p in percentages
    ]
    # (TODO) Get the accuracy when using both basic and advanced features
    combined_accuracy = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    # Plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(percentages, basic_accuracy, label="Basic features", marker=".")
    ax.plot(percentages, advanced_accuracy, label="Advanced features", marker=".")
    ax.plot(percentages, combined_accuracy, label="Combined features", marker=".")
    ax.set_xlim(5, 105)
    # ax.set_ylim(0.5, 1)
    ax.set_xlabel("Percentage of training data")
    ax.set_ylabel("Accuracy")
    ax.legend()
    plt.show()
