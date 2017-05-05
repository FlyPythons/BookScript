#!/usr/bin/env python


from math import log2
import operator


def calc_shannon_ent(data_mat):
    num = len(data_mat)
    label_counts = {}
    for vec in data_mat:
        label = vec[-1]
        label_counts[label] = label_counts.get(label, 0) + 1
        # print(vec)

    # print(num)

    shannon_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key])/num
        shannon_ent -= prob*log2(prob)

    return shannon_ent


def split_data_mat(data_mat, axis, value):
    ret_data_mat = []
    for vec in data_mat:
        if vec[axis] == value:
            reduced_vec = vec[:axis]
            reduced_vec.extend(vec[axis+1:])
            ret_data_mat.append(reduced_vec)

    return ret_data_mat


def choose_feat(data_mat):
    feat_num = len(data_mat[0]) - 1
    ent_base = calc_shannon_ent(data_mat)
    info_gain_best = 0.0
    best_feat = -1

    for i in range(feat_num):
        feat_list = [exam[i] for exam in data_mat]
        feat_set = set(feat_list)
        ent_new = 0.0

        for value in feat_set:
            sub_data_mat = split_data_mat(data_mat, i, value)
            prob = len(sub_data_mat)/float(len(data_mat))
            ent_new += prob*calc_shannon_ent(sub_data_mat)

        info_gain = ent_base - ent_new
        # print("the info gain of feature %s is %s" % (i, info_gain))
        if info_gain > info_gain_best:
            info_gain_best = info_gain
            best_feat = i

    return best_feat


def create_data_mat():
    data_mat = [[1, 1, 'yes'],
                [1, 1, 'yes'],
                [1, 0, 'no'],
                [0, 1, 'no'],
                [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return data_mat, labels


def major_class(class_list):
    class_counts = {}
    for vote in class_list:
        class_counts[vote] = class_counts.get(vote, 0) + 1
        sorted_class_count = sorted(class_counts, key=operator.itemgetter(1), reverse=True)

    # print(sorted_class_count)
    return sorted_class_count[0][0]


def create_tree(data_mat, labels):
    class_list = [exam[-1] for exam in data_mat]
    if class_list.count(class_list[0]) == len(class_list):  # same items
        return class_list[0]

    if len(data_mat[0]) == 1:  # data_mat m x 1
        return major_class(class_list)

    best_feat = choose_feat(data_mat)
    best_feat_label = labels[best_feat]
    mytree = {best_feat_label: {}}
    del labels[best_feat]
    feat_list = [exam[best_feat] for exam in data_mat]
    feat_set = set(feat_list)
    for value in feat_set:
        sublabels = labels[:]
        mytree[best_feat_label][value] = create_tree(split_data_mat(data_mat, best_feat, value), sublabels)

    return mytree


def classify(input_tree, feat_labels, test_vec):
    first_str = list(input_tree.keys())[0]
    second_dict = input_tree[first_str]
    feat_index = feat_labels.index(first_str)
    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if isinstance(second_dict[key], dict):
                class_label = classify(second_dict[key], feat_labels, test_vec)
            else:
                class_label = second_dict[key]

    return class_label


def store_tree(input_tree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(input_tree, fw)
    fw.close()


def grab_tree(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)


def main():
    # data_mat, labels = create_data_mat()
    # shannon = calc_shannon_ent(data_mat)
    # print(create_tree(data_mat, labels))
    fr = open('lenses.txt', 'r')
    data_mat = [line.strip().split('\t') for line in fr.readlines()]
    labels = ['age', 'prescript', 'astigmatic', 'tearRate']
    mytree = create_tree(data_mat, labels)
    print(mytree)
    import TreeViewer
    TreeViewer.create_plot(mytree)
    store_tree(mytree, "classifierStorage.txt")
    print(grab_tree("classifierStorage.txt"))


if __name__ == "__main__":
    main()

