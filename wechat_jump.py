#!/usr/bin/env python
# encoding=utf-8
"""
created by maxuewei2
"""
from PIL import Image, ImageFilter
import os
import math
import time

"""
针对分辨率为1920*1080，分辨率不同请自行修改代码

"""

man_colors = [[85, 77, 125], [64, 66, 91], [86, 76, 124], [64, 51, 86], [54, 60, 102]]
man_colors = [tuple(x) for x in man_colors]
center_point = (560, 980)
Y = 1920
X = 1080


def distance(a, b):
    return sum([(a[i] - b[i])**2 for i in range(len(a))])


def is_equal(a, b):
    return sum(distance(a[i], b[i]) for i in range(len(a))) < 200


def get_man_point(rgb_im):
    bias_nums = [35, 31, 60, 58]
    for y in range(700, Y):
        for x in range(X):
            bias = 0
            color = rgb_im.getpixel((x, y))
            if distance(color, man_colors[0]) > 50:
            	continue
            colors = []
            colors.append(color)
            for bias_n in bias_nums:
                bias += bias_n
                if y + bias >= Y:
                    break
                colors.append(rgb_im.getpixel((x, y + bias)))
            if is_equal(colors, man_colors):
                y = y + bias - 9
                return (x, y)
    print('没能找到小人位置，请手动跳一次然后再次运行本程序')
    exit(0)
    


def get_highest_point(rgb_im, man_point):
    if man_point[0] < center_point[0]:
        start, end = center_point[0], X
    else:
        start, end = 0, center_point[0]
    for i in range(300, Y):
        for j in range(start, end):
            if distance(rgb_im.getpixel((j, i)), rgb_im.getpixel((start, i))) > 300:
                return (j, i)


def get_dest_point(man_point, center_point, highest_x):
    slope = (man_point[1] - center_point[1]) / (man_point[0] - center_point[0])
    bias = man_point[1] - (slope * man_point[0])
    dest_y = slope * highest_x + bias
    return (highest_x, dest_y)


if __name__ == '__main__':
    scs = os.listdir('.')
    scs = [x for x in scs if x.startswith('sc_')]
    scs = [x[3:-4] for x in scs]
    scs = [int(x) for x in scs]
    start_num = max(scs) + 1 if scs else 0
    print('screenshot file name starts from ', start_num)
    for i in range(10000):
        print('第 %d 跳' %(i+1))
        imgname = 'sc_' + str(start_num + i) + '.png'
        os.system('adb shell screencap -p |sed \'s/\r$//\'>' + imgname)
        im = Image.open(imgname)
        rgb_im = im.convert('RGB')
        man_p = get_man_point(rgb_im)
        print('小人:\t', man_p)
        highest_p = get_highest_point(rgb_im, man_p)
        print('最高点:\t', highest_p)
        dest_p = get_dest_point(man_p, center_point, highest_p[0])
        print('目标点:\t' ,dest_p)
        press_time = int(math.sqrt((man_p[0] - dest_p[0])**2 + (man_p[1] - dest_p[1])**2) * 1.363)
        os.system('adb shell input swipe 500 500 500 500 ' + str(press_time))
        time.sleep(2)
