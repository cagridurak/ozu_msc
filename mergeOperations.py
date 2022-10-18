#!/usr/bin/env python

import csv

import os
import shutil

import numpy as np
#merge_matrix_excel[][]

with open('dependency_matrix.csv', newline='') as csvfile:
    dep_matrix = list(csv.reader(csvfile))

with open('commit_counts.csv', newline='') as csvfile:
    count_matrix = list(csv.reader(csvfile))

import argparse
parser = argparse.ArgumentParser(description='dependency finder arguments')
parser.add_argument("-p", type=int, required=True, help="kactan fazla beraber commitlenen classlar yazdirilsin?")

args = parser.parse_args()

#print('args.p:', args.p)


pure_list = []
pl = open('pureList', 'r')
for line in pl:
    pure_list.append(line)

item_count = len(pure_list)

merge_matrix_excel = [ [ 0 for i in range(item_count+1) ] for j in range(item_count+1) ]

for x in range(item_count+1):
    for y in range(item_count+1):
        if(dep_matrix[x][y] == ''):
            if(x!=0 and y!=0):
                if(int(count_matrix[x][y]) > args.p):
                    #print(count_matrix[x][y] + " is bigger than " + str(args.p))
                    #print(count_matrix[y][x])
                    #print(dep_matrix[y][x])
                    if (dep_matrix[y][x] == ''):
                        merge_matrix_excel[x][y] = count_matrix[x][y] + ' MV'
                    else:
                        merge_matrix_excel[x][y] = count_matrix[x][y]
                else:
                    merge_matrix_excel[x][y] = count_matrix[x][y]
            else:
                merge_matrix_excel[x][y] = count_matrix[x][y]
        else:
            if(x==0 or y==0):
                merge_item = dep_matrix[x][y] + count_matrix[x][y]
            else:
                merge_item = dep_matrix[x][y] + '-' + count_matrix[x][y]
            merge_matrix_excel[x][y] = merge_item

np.savetxt("merge.csv", merge_matrix_excel, delimiter=",", fmt='%s')