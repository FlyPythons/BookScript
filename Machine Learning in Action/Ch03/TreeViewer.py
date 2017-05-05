#!/usr/bin/env python


import matplotlib.pyplot as plt


DECISION_NODE = {"boxstyle": "sawtooth",
                 "fc": "0.8"}
LEAF_NODE = {"boxstyle": "round4",
             "fc": "0.8"}
ARROW = {"arrowstyle": "<-"}


def get_num_leafs(mytree):
    num_leafs = 0
    first_str = list(mytree.keys())[0]
    second_dict = mytree[first_str]

    for key in second_dict.keys():
        if isinstance(second_dict[key], dict):
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1

    return num_leafs


def get_tree_depth(mytree):
    max_depth = 0
    first_str = list(mytree.keys())[0]
    second_dict = mytree[first_str]
    for key in second_dict.keys():
        if isinstance(second_dict[key], dict):
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth

    return max_depth


def plot_node(text, center_pos, parent_pos, style):
    create_plot.ax1.annotate(text, xy=parent_pos,
                        xycoords='axes fraction', xytext=center_pos,
                        textcoords='axes fraction', va="center",
                        ha="center", bbox=style, arrowprops=ARROW )


def plot_mid_text(center_pos, parent_pos, text):
    x = (parent_pos[0] + center_pos[0])/2.0
    y = (parent_pos[1] + center_pos[1])/2.0
    create_plot.ax1.text(x, y, text)


def plot_tree(mytree, parent_pos, text):
    num_leafs = get_num_leafs(mytree)
    first_str = list(mytree.keys())[0]
    center_pos = (plot_tree.x_off + (1.0 + num_leafs)/2.0/plot_tree.width, plot_tree.y_off)
    plot_mid_text(center_pos, parent_pos, text)
    plot_node(first_str, center_pos, parent_pos, DECISION_NODE)
    second_dict = mytree[first_str]
    plot_tree.y_off -= 1.0/plot_tree.depth
    for key in second_dict.keys():
        if isinstance(second_dict[key], dict):
            plot_tree(second_dict[key], center_pos, str(key))
        else:
            plot_tree.x_off += 1.0/plot_tree.width
            plot_node(second_dict[key], (plot_tree.x_off, plot_tree.y_off), center_pos, LEAF_NODE)
            plot_mid_text((plot_tree.x_off, plot_tree.y_off), center_pos, str(key))

    plot_tree.y_off += 1.0/plot_tree.depth


def create_plot(mytree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = {"xticks": [],
               "yticks": []}
    create_plot.ax1 = plt.subplot(111, frameon=False,)    # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plot_tree.width = float(get_num_leafs(mytree))
    plot_tree.depth = float(get_tree_depth(mytree))
    print(plot_tree.depth, plot_tree.width)
    plot_tree.x_off = -0.5/plot_tree.width
    plot_tree.y_off = 1.0
    plot_tree(mytree, (0.5, 1.0), 'xxx')
    plt.show()


def retrieve_tree(i):
    tree_list = [{'no surfacing ': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}, 3: 'maybe'}},
                 {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                 ]
    return tree_list[i]





def main():
    mytree = retrieve_tree(0)
    #print(get_num_leafs(mytree), get_tree_depth(mytree))
    #create_plot(mytree)


if __name__ == "__main__":
    main()

