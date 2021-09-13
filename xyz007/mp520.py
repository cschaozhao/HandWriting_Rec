import inspect
import sys
import math
import numpy as np
import scipy.stats as st

"""
Raise a "not defined" exception as a reminder 
"""


def _raise_not_defined():
    print("Method not implemented: %s" % inspect.stack()[1][3])
    sys.exit(1)


"""
Extract 'basic' features, i.e., whether a pixel is background or
forground (part of the digit) 
"""


def extract_basic_features(digit_data, width, height):
    features = []
    for i in range(height):
        for j in range(width):
            if digit_data[i][j] == 0:
                features.append(False)
            else:
                features.append(True)
    return features


"""
Extract advanced features that you will come up with 
"""


def extract_advanced_features(digit_data, width, height):
    features = []
    features = [[], [], []]

    for i in range(height):
        for j in range(width):
            if digit_data[i][j] != 0:
                cut = i
                break
        if digit_data[i][j] != 0:
            break
    count_cut = 0
    new_digit_data = []
    for i in range(height):
        if (cut + i) < height:
            new_digit_data.append(digit_data[cut + i])
        else:
            new_digit_data.append(digit_data[0])

    # feature set 1: set 4*4 pixels as a unit, count its number, " "=0,"+"=1,"#"=2
    w = int(width / 4)
    h = int(height / 4)
    count = 0
    for i in range(h):
        for j in range(w):
            for k in range(4 * i, 4 * i + 4):
                for l in range(4 * j, 4 * j + 4):
                    count = count + new_digit_data[k][l]
            if count > 3:
                features[0].append(True)
            else:
                features[0].append(False)
            count = 0

    # feature set 2:横向扫描,直方图，应用正态分布
    count_width = 0
    for i in range(height):
        for j in range(width):
            count_width = count_width + new_digit_data[i][j]
        features[1].append(count_width)
        count_width = 0

    # feature set 3：将整张照片分成4份分别计算各份的数值
    count_quarter = 0
    half_wigth = int(width / 2)
    half_height = int(height / 2)
    for i in range(1, 3):
        for j in range(1, 3):
            for hh in range((i - 1) * half_height, i * half_height):
                for hw in range((j - 1) * half_wigth, j * half_wigth):
                    count_quarter = count_quarter + new_digit_data[hh][hw]
            features[2].append(count_quarter)
            count_quarter = 0

    return features


"""
Extract the final features that you would like to use
"""


def extract_final_features(digit_data, width, height):
    features = []
    features = [[], [], []]

    for i in range(height):
        for j in range(width):
            if digit_data[i][j] != 0:
                cut = i
                break
        if digit_data[i][j] != 0:
            break
    count_cut = 0
    new_digit_data = []
    for i in range(height):
        if (cut + i) < height:
            new_digit_data.append(digit_data[cut + i])
        else:
            new_digit_data.append(digit_data[0])

    # feature set 1: set 4*4 pixels as a unit, count its number, " "=0,"+"=1,"#"=2
    w = int(width / 4)
    h = int(height / 4)
    count = 0
    for i in range(h):
        for j in range(w):
            for k in range(4 * i, 4 * i + 4):
                for l in range(4 * j, 4 * j + 4):
                    count = count + new_digit_data[k][l]
            if count > 3:
                features[0].append(True)
            else:
                features[0].append(False)
            count = 0

    # feature set 2:横向扫描,直方图，应用正态分布
    count_width = 0
    for i in range(height):
        for j in range(width):
            count_width = count_width + new_digit_data[i][j]
        features[1].append(count_width)
        count_width = 0

    # feature set 3：将整张照片分成4份分别计算各份的数值
    count_quarter = 0
    half_wigth = int(width / 2)
    half_height = int(height / 2)
    for i in range(1, 3):
        for j in range(1, 3):
            for hh in range((i - 1) * half_height, i * half_height):
                for hw in range((j - 1) * half_wigth, j * half_wigth):
                    count_quarter = count_quarter + new_digit_data[hh][hw]
            features[2].append(count_quarter)
            count_quarter = 0

    features.append(extract_basic_features(digit_data, width, height))
    return features


"""
Compupte the parameters including the prior and and all the P(x_i|y). Note
that the features to be used must be computed using the passed in method
feature_extractor, which takes in a single digit data along with the width
and height of the image. For example, the method extract_basic_features
defined above is a function than be passed in as a feature_extractor
implementation.

The percentage parameter controls what percentage of the example data
should be used for training. 
"""


def compute_statistics(data, label, width, height, feature_extractor, percentage=100.0):
    length = int(len(label) * percentage / 100)
    k = 1
    global prior
    prior = []
    global P
    P = [[], [], [], [], [], [], [], [], [], []]
    figure_image = []
    P_count = []
    a0 = []
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []
    a9 = []

    # initialize P_count
    for i in range(width * height):
        a0.append(0)
        a1.append(0)
        a2.append(0)
        a3.append(0)
        a4.append(0)
        a5.append(0)
        a6.append(0)
        a7.append(0)
        a8.append(0)
        a9.append(0)

    P_count.append(a0)
    P_count.append(a1)
    P_count.append(a2)
    P_count.append(a3)
    P_count.append(a4)
    P_count.append(a5)
    P_count.append(a6)
    P_count.append(a7)
    P_count.append(a8)
    P_count.append(a9)
    # compute the basic features
    if feature_extractor == extract_basic_features:
        # compute the prior

        # compute P and prior

        counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(length):
            if label[i] == 0:
                counter[0] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[0][j] += 1
            elif label[i] == 1:
                counter[1] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[1][j] += 1
            elif label[i] == 2:
                counter[2] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[2][j] += 1
            elif label[i] == 3:
                counter[3] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[3][j] += 1
            elif label[i] == 4:
                counter[4] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[4][j] += 1
            elif label[i] == 5:
                counter[5] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[5][j] += 1
            elif label[i] == 6:
                counter[6] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[6][j] += 1
            elif label[i] == 7:
                counter[7] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[7][j] += 1
            elif label[i] == 8:
                counter[8] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[8][j] += 1
            elif label[i] == 9:
                counter[9] += 1
                figure_image = feature_extractor(data[i], width, height)
                for j in range(len(figure_image)):
                    if figure_image[j]:
                        P_count[9][j] += 1
        for i in range(10):
            prior.append(counter[i] / length)
            for j in range(width * height):
                P[i].append((P_count[i][j] + k) / (counter[i] + 2 * k))
    # compute the advanced features
    else:
        global sigma_feature_2
        global sigma_feature_3
        sigma_feature_3 = [[], [], [], [], [], [], [], [], [], []]
        sigma_feature_2 = [[], [], [], [], [], [], [], [], [], []]
        sigma_height = [[], [], [], [], [], [], [], [], [], []]
        for j in range(10):
            for i in range(height):
                sigma_height[j].append([])
        sigma_four = [[], [], [], [], [], [], [], [], [], []]
        for j in range(10):
            for i in range(4):
                sigma_four[j].append([])
        global P_advanced
        P_advanced = [[[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []],
                      [[], [], []], [[], [], []], [[], [], []], [[], [], []]]
        P_advanced_count = [[], [], [], [], [], [], [], [], [], []]
        b0 = []
        b1 = []
        b2 = []
        b3 = []
        b4 = []
        b5 = []
        b6 = []
        b7 = []
        b8 = []
        b9 = []

        for i in range(int(width * height / 16)):
            b0.append(0)
            b1.append(0)
            b2.append(0)
            b3.append(0)
            b4.append(0)
            b5.append(0)
            b6.append(0)
            b7.append(0)
            b8.append(0)
            b9.append(0)
        P_advanced_count[0].append(b0)
        P_advanced_count[1].append(b1)
        P_advanced_count[2].append(b2)
        P_advanced_count[3].append(b3)
        P_advanced_count[4].append(b4)
        P_advanced_count[5].append(b5)
        P_advanced_count[6].append(b6)
        P_advanced_count[7].append(b7)
        P_advanced_count[8].append(b8)
        P_advanced_count[9].append(b9)

        c0 = []
        c1 = []
        c2 = []
        c3 = []
        c4 = []
        c5 = []
        c6 = []
        c7 = []
        c8 = []
        c9 = []
        for i in range(height):
            c0.append(0)
            c1.append(0)
            c2.append(0)
            c3.append(0)
            c4.append(0)
            c5.append(0)
            c6.append(0)
            c7.append(0)
            c8.append(0)
            c9.append(0)
        P_advanced_count[0].append(c0)
        P_advanced_count[1].append(c1)
        P_advanced_count[2].append(c2)
        P_advanced_count[3].append(c3)
        P_advanced_count[4].append(c4)
        P_advanced_count[5].append(c5)
        P_advanced_count[6].append(c6)
        P_advanced_count[7].append(c7)
        P_advanced_count[8].append(c8)
        P_advanced_count[9].append(c9)

        P_advanced_count[0].append([0, 0, 0, 0])
        P_advanced_count[1].append([0, 0, 0, 0])
        P_advanced_count[2].append([0, 0, 0, 0])
        P_advanced_count[3].append([0, 0, 0, 0])
        P_advanced_count[4].append([0, 0, 0, 0])
        P_advanced_count[5].append([0, 0, 0, 0])
        P_advanced_count[6].append([0, 0, 0, 0])
        P_advanced_count[7].append([0, 0, 0, 0])
        P_advanced_count[8].append([0, 0, 0, 0])
        P_advanced_count[9].append([0, 0, 0, 0])

        counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(length):
            if label[i] == 0:
                counter[0] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced)==4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[0][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[0][0][j] += 1
                for j in range(height):
                    # 计算平均数
                    P_advanced_count[0][1][j] += feature_advanced[1][j]
                    # 计算方差
                    sigma_height[0][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[0][2][j] += feature_advanced[2][j]
                    sigma_four[0][j].append(feature_advanced[2][j])
            elif label[i] == 1:
                counter[1] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[1][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[1][0][j] += 1
                for j in range(height):
                    P_advanced_count[1][1][j] += feature_advanced[1][j]
                    sigma_height[1][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[1][2][j] += feature_advanced[2][j]
                    sigma_four[1][j].append(feature_advanced[2][j])
            elif label[i] == 2:
                counter[2] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[2][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[2][0][j] += 1
                for j in range(height):
                    P_advanced_count[2][1][j] += feature_advanced[1][j]
                    sigma_height[2][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[2][2][j] += feature_advanced[2][j]
                    sigma_four[2][j].append(feature_advanced[2][j])
            elif label[i] == 3:
                counter[3] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[3][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[3][0][j] += 1
                for j in range(height):
                    P_advanced_count[3][1][j] += feature_advanced[1][j]
                    sigma_height[3][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[3][2][j] += feature_advanced[2][j]
                    sigma_four[3][j].append(feature_advanced[2][j])
            elif label[i] == 4:
                counter[4] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[4][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[4][0][j] += 1
                for j in range(height):
                    P_advanced_count[4][1][j] += feature_advanced[1][j]
                    sigma_height[4][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[4][2][j] += feature_advanced[2][j]
                    sigma_four[4][j].append(feature_advanced[2][j])
            elif label[i] == 5:
                counter[5] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[5][j] += 1
                for j in range(int(width * height / 16)):
                    if feature_advanced[0][j]:
                        P_advanced_count[5][0][j] += 1
                for j in range(height):
                    P_advanced_count[5][1][j] += feature_advanced[1][j]
                    sigma_height[5][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[5][2][j] += feature_advanced[2][j]
                    sigma_four[5][j].append(feature_advanced[2][j])
            elif label[i] == 6:
                counter[6] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[6][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[6][0][j] += 1
                for j in range(height):
                    P_advanced_count[6][1][j] += feature_advanced[1][j]
                    sigma_height[6][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[6][2][j] += feature_advanced[2][j]
                    sigma_four[6][j].append(feature_advanced[2][j])
            elif label[i] == 7:
                counter[7] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[7][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[7][0][j] += 1
                for j in range(height):
                    P_advanced_count[7][1][j] += feature_advanced[1][j]
                    sigma_height[7][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[7][2][j] += feature_advanced[2][j]
                    sigma_four[7][j].append(feature_advanced[2][j])
            elif label[i] == 8:
                counter[8] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[8][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[8][0][j] += 1
                for j in range(height):
                    P_advanced_count[8][1][j] += feature_advanced[1][j]
                    sigma_height[8][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[8][2][j] += feature_advanced[2][j]
                    sigma_four[8][j].append(feature_advanced[2][j])
            elif label[i] == 9:
                counter[9] += 1
                feature_advanced = feature_extractor(data[i], width, height)
                if len(feature_advanced) == 4:
                    for j in range(len(feature_advanced[3])):
                        if feature_advanced[3][j]:
                            P_count[9][j] += 1
                for j in range(len(feature_advanced[0])):
                    if feature_advanced[0][j]:
                        P_advanced_count[9][0][j] += 1
                for j in range(height):
                    P_advanced_count[9][1][j] += feature_advanced[1][j]
                    sigma_height[9][j].append(feature_advanced[1][j])
                for j in range(len(feature_advanced[2])):
                    P_advanced_count[9][2][j] += feature_advanced[2][j]
                    sigma_four[9][j].append(feature_advanced[2][j])

        for i in range(10):
            prior.append(counter[i] / length)
            for j in range(width * height):
                P[i].append((P_count[i][j] + k) / (counter[i] + 2 * k))
            for j in range(int(width * height / 16)):
                P_advanced[i][0].append((P_advanced_count[i][0][j] + k) / (counter[i] + 2 * k))
            for j in range(height):
                # 计算均值 mean
                P_advanced[i][1].append(P_advanced_count[i][1][j] / counter[i])
                # 计算方差
                if np.std(sigma_height[i][j], axis=0, ddof=1) == 0:
                    sigma_feature_2[i].append(0.1)
                else:
                    sigma_feature_2[i].append(np.std(sigma_height[i][j], axis=0, ddof=1))
            for j in range(4):
                # 计算均值
                P_advanced[i][2].append(P_advanced_count[i][2][j] / counter[i])
                # 计算方差
                if np.std(sigma_four[i][j], axis=0, ddof=1) == 0:
                    sigma_feature_3[i].append(0.1)
                else:
                    sigma_feature_3[i].append(np.std(sigma_four[i][j], axis=0, ddof=1))


def compute_class(features):
    predicted = -1
    log_P = [math.log(prior[0]), math.log(prior[1]), math.log(prior[2]), math.log(prior[3]), math.log(prior[4]),
             math.log(prior[5]), math.log(prior[6]), math.log(prior[7]), math.log(prior[8]), math.log(prior[9])]
    if len(features) < 10:
        if len(features)==4:
            for i in range(len(features[3])):
                if features[3][i] == True:
                    log_P[0] += math.log(P[0][i])
                    log_P[1] += math.log(P[1][i])
                    log_P[2] += math.log(P[2][i])
                    log_P[3] += math.log(P[3][i])
                    log_P[4] += math.log(P[4][i])
                    log_P[5] += math.log(P[5][i])
                    log_P[6] += math.log(P[6][i])
                    log_P[7] += math.log(P[7][i])
                    log_P[8] += math.log(P[8][i])
                    log_P[9] += math.log(P[9][i])
                else:
                    log_P[0] += math.log(1 - P[0][i])
                    log_P[1] += math.log(1 - P[1][i])
                    log_P[2] += math.log(1 - P[2][i])
                    log_P[3] += math.log(1 - P[3][i])
                    log_P[4] += math.log(1 - P[4][i])
                    log_P[5] += math.log(1 - P[5][i])
                    log_P[6] += math.log(1 - P[6][i])
                    log_P[7] += math.log(1 - P[7][i])
                    log_P[8] += math.log(1 - P[8][i])
                    log_P[9] += math.log(1 - P[9][i])
        # 计算advancedfeature set1：
        for i in range(len(features[0])):
            if features[0][i] == True:
                log_P[0] += math.log(P_advanced[0][0][i])
                log_P[1] += math.log(P_advanced[1][0][i])
                log_P[2] += math.log(P_advanced[2][0][i])
                log_P[3] += math.log(P_advanced[3][0][i])
                log_P[4] += math.log(P_advanced[4][0][i])
                log_P[5] += math.log(P_advanced[5][0][i])
                log_P[6] += math.log(P_advanced[6][0][i])
                log_P[7] += math.log(P_advanced[7][0][i])
                log_P[8] += math.log(P_advanced[8][0][i])
                log_P[9] += math.log(P_advanced[9][0][i])
            else:
                log_P[0] += math.log(1 - P_advanced[0][0][i])
                log_P[1] += math.log(1 - P_advanced[1][0][i])
                log_P[2] += math.log(1 - P_advanced[2][0][i])
                log_P[3] += math.log(1 - P_advanced[3][0][i])
                log_P[4] += math.log(1 - P_advanced[4][0][i])
                log_P[5] += math.log(1 - P_advanced[5][0][i])
                log_P[6] += math.log(1 - P_advanced[6][0][i])
                log_P[7] += math.log(1 - P_advanced[7][0][i])
                log_P[8] += math.log(1 - P_advanced[8][0][i])
                log_P[9] += math.log(1 - P_advanced[9][0][i])

        # compute advanced feature set 2
        for i in range(len(features[1])):
            log_P[0] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[0][1][i], scale=sigma_feature_2[0][i]))
            log_P[1] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[1][1][i], scale=sigma_feature_2[1][i]))
            log_P[2] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[2][1][i], scale=sigma_feature_2[2][i]))
            log_P[3] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[3][1][i], scale=sigma_feature_2[3][i]))
            log_P[4] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[4][1][i], scale=sigma_feature_2[4][i]))
            log_P[5] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[5][1][i], scale=sigma_feature_2[5][i]))
            log_P[6] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[6][1][i], scale=sigma_feature_2[6][i]))
            log_P[7] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[7][1][i], scale=sigma_feature_2[7][i]))
            log_P[8] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[8][1][i], scale=sigma_feature_2[8][i]))
            log_P[9] += math.log(st.norm.pdf(features[1][i], loc=P_advanced[9][1][i], scale=sigma_feature_2[9][i]))

        # compute advanced feature set 3
        for i in range(len(features[2])):
            log_P[0] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[0][2][i], scale=sigma_feature_3[0][i]))
            log_P[1] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[1][2][i], scale=sigma_feature_3[1][i]))
            log_P[2] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[2][2][i], scale=sigma_feature_3[2][i]))
            log_P[3] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[3][2][i], scale=sigma_feature_3[3][i]))
            log_P[4] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[4][2][i], scale=sigma_feature_3[4][i]))
            log_P[5] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[5][2][i], scale=sigma_feature_3[5][i]))
            log_P[6] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[6][2][i], scale=sigma_feature_3[6][i]))
            log_P[7] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[7][2][i], scale=sigma_feature_3[7][i]))
            log_P[8] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[8][2][i], scale=sigma_feature_3[8][i]))
            log_P[9] += math.log(st.norm.pdf(features[2][i], loc=P_advanced[9][2][i], scale=sigma_feature_3[9][i]))
        max_P = max(log_P)
        predicted = log_P.index(max_P)

    else:
        # 计算basic情况的数字
        for i in range(len(features)):
            if features[i] == True:
                log_P[0] += math.log(P[0][i])
                log_P[1] += math.log(P[1][i])
                log_P[2] += math.log(P[2][i])
                log_P[3] += math.log(P[3][i])
                log_P[4] += math.log(P[4][i])
                log_P[5] += math.log(P[5][i])
                log_P[6] += math.log(P[6][i])
                log_P[7] += math.log(P[7][i])
                log_P[8] += math.log(P[8][i])
                log_P[9] += math.log(P[9][i])
            else:
                log_P[0] += math.log(1 - P[0][i])
                log_P[1] += math.log(1 - P[1][i])
                log_P[2] += math.log(1 - P[2][i])
                log_P[3] += math.log(1 - P[3][i])
                log_P[4] += math.log(1 - P[4][i])
                log_P[5] += math.log(1 - P[5][i])
                log_P[6] += math.log(1 - P[6][i])
                log_P[7] += math.log(1 - P[7][i])
                log_P[8] += math.log(1 - P[8][i])
                log_P[9] += math.log(1 - P[9][i])
        max_P = max(log_P)
        predicted = log_P.index(max_P)
    return predicted


"""
Compute joint probaility for all the classes and make predictions for a list
of data
"""


def classify(data, width, height, feature_extractor):
    predicted = []
    feature_data = []
    for i in range(len(data)):
        feature_data = feature_extractor(data[i], width, height)
        predicted.append(compute_class(feature_data))
        feature_data.clear()
    return predicted
