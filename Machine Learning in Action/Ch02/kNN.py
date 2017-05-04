#!/usr/bin/env python


from numpy import *
import matplotlib.pyplot as plt
import operator
from os import listdir


def create_data():
    """
    create train data
    :return:
    """
    group = array([[1.0, 1.1],
                  [1.0, 1.0],
                  [0, 0],
                  [0, 0.1]
                  ])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(x, data, labels, k):
    """

    :param x: the input vector to classify
    :param data: full matrix of training examples
    :param labels: vector of labels
    :param k: the number of nearest neighbors to use in the voting
    :return:
    """
    # distance calculation
    data_size = data.shape[0]
    diff_mat = tile(x, (data_size, 1)) - data
    sq_diff_mat = diff_mat**2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances**0.5

    # voting with lowest k distances
    sorted_dist_ind = distances.argsort()  # sort list distances and return indices
    # print(data_size, distances, sorted_dist_ind)
    class_count = {}  # class: num of class
    for i in range(k):
        vote_label = labels[sorted_dist_ind[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1  # get dict item of key 'vote_label' , default 0

    # sort dict class_count
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    #print(class_count, sorted_class_count)

    return sorted_class_count[0][0]


def plot(group, labels, vec):
    """
    plot scatter of the result
    :param group:
    :param labels:
    :param vec:
    :return:
    """
    x = group.T[0].tolist()
    x.append(vec[0])
    y = group.T[1].tolist()
    y.append(vec[1])
    labels.append('Input')
    print(x)
    plt.scatter(x, y)
    for i in range(len(x)):
        plt.annotate(labels[i], xy=(x[i], y[i]), xytext=(0, 10), textcoords='offset points', ha='center', va='top')
    plt.show()


def file2matrix(filename):
    love_dict = {'largeDoses': 3, 'smallDoses': 2, 'didntLike': 1}
    fr = open(filename)
    lines = fr.readlines()
    line_num = len(lines)
    return_mat = zeros((line_num, 3))  # line_num x 3 matrix
    class_label = []
    n = 0
    for line in lines:
        line = line.strip()
        list_from_line = line.split("\t")
        return_mat[n, :] = list_from_line[0:3]
        class_label.append(love_dict.get(list_from_line[-1]))
        n += 1

    return return_mat, class_label


def auto_norm(data):
    min_nums = data.min(0)
    max_nums = data.max(0)
    ranges = max_nums - min_nums
    norm_data = zeros(shape(data))
    m = data.shape[0]
    norm_data = data - tile(min_nums, (m, 1))
    norm_data = norm_data/tile(ranges, (m, 1))

    return norm_data, ranges, min_nums


def data_class_test():
    ho_ratio = 0.10
    data_mat, data_labels = file2matrix('datingTestSet.txt')
    norm_data, ranges, min_nums = auto_norm(data_mat)
    m = norm_data.shape[0]
    test_num = int(m*ho_ratio)
    error_num = 0.0
    for i in range(test_num):
        classify_result = classify0(norm_data[i, :], norm_data[test_num:m, :], data_labels[test_num:m], 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classify_result, data_labels[i]))

        if classify_result != data_labels[i]:
            error_num += 1.0
        else:
            pass

    print("error num is: %d. test num is: %d. the total error rate is: %f" % (error_num, test_num, (error_num/float(test_num))))


def classify_person():
    result_list = ['not at all', 'in small doses', 'in large doses']
    percent_tat = float(input("percentage of time spent playing video games?"))
    ff_miles = float(input("frequent flier miles earned per year?"))
    icecream = float(input("liters of ice cream consumed per year?"))
    data_mat, data_labels = file2matrix('datingTestSet2.txt')
    norm_data, ranges, min_nums = auto_norm(data_mat)
    data = array([ff_miles, percent_tat, icecream, ])
    classify_result = classify0((data - min_nums)/ranges, norm_data, data_abels, 3)
    print("You will probably like this person: %s" % result_list[classify_result - 1])


def img2mat(filename):
    return_mat = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            return_mat[0, 32*i+j] = line[j]

    return return_mat


def handwriting_test():
    labels = []
    train_list = listdir('trainingDigits')
    m = len(train_list)
    train_mat = zeros((m, 1024))
    for i in range(m):
        filename = train_list[i]
        file_str = filename.split('.')[0]
        class_num = int(file_str.split('_')[0])
        labels.append(class_num)
        train_mat[i, :] = img2mat('trainingDigits/%s' % filename)

    test_list = listdir('testDigits')
    error_num = 0.0
    m_test = len(test_list)
    for i in range(m_test):
        filename = test_list[i]
        file_str = filename.split('.')[0]
        class_num = int(file_str.split('_')[0])
        data = img2mat('testDigits/%s' % filename)
        classify_result = classify0(data, train_mat, labels, 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classify_result, class_num))
        if classify_result != class_num:
            error_num += 1.0
        else:
            pass

    print("error num is: %d. test num is: %d. the total error rate is: %f" % (error_num, m_test, (error_num /float(m_test))))

def main():
    group, labels = create_data()
    class_name = classify0([0, 0], group, labels, 3)
    #print(class_name)
    # plot(group, labels, [0, 0])

    data_mat, data_labels = file2matrix("datingTestSet.txt")

    # fig = plt.figure()
    # ax = fig.add_subplot(111)

    # print(data_mat[:, 1])
    # ax.scatter(data_mat[:, 1], data_mat[:, 2], 15.0*array(data_labels), 15.0*array(data_labels))
    # ax.scatter(data_mat[:, 0], data_mat[:, 1], 15.0 * array(data_labels), 15.0 * array(data_labels))

    # plt.show()

    # norm_data, ranges, min_nums = auto_norm(data_mat)
    # data_class_test()
    handwriting_test()


if __name__ == "__main__":
    main()
