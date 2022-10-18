#!/usr/bin/env python

import os
import shutil

import argparse
parser = argparse.ArgumentParser(description='dependency finder arguments')
parser.add_argument("-p", type=int, required=True, help="kactan fazla beraber commitlenen classlar yazdirilsin?")

args = parser.parse_args()

#print('args.p:', args.p)

pure_list = []
contains = 0
path_no_need = "no_need"
commit_list = []

isExist = os.path.exists(path_no_need)
#print(isExist)
if not isExist:
    os.mkdir(path_no_need)

#txtlerin icinden nokta olan satirlari cikaran dongu
txt_files = [x for x in os.listdir(".") if x.endswith(".txt")]
for file_name in txt_files:
    with open(file_name, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != " M      .\n":
                f.write(i)
        f.truncate()

#txtlerin satir baslarinda M... A... D... olan satirlari cikaran dongu
txt_files = [x for x in os.listdir(".") if x.endswith(".txt")]
for file_name in txt_files:
    with open(file_name, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            #print("i[:8] "+i[:8])
            if (i[1:8] == "       "):
                #print("..." + i[1:8] + "...")
                #print(i[8:])
                f.write(i[8:])
        f.truncate()

#txtlerin hpp uzantilarini cpp yapan dongu
txt_files = [x for x in os.listdir(".") if x.endswith(".txt")]
for file_name in txt_files:
    with open(file_name, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            #print("i[-4:] "+i[-4:])
            #print("i[:-4] "+i[:-4])
            new_i = i[:-4] + "cpp\n"
            f.write(new_i)

#txtlerde ayni isimli classlardan 1 tane yazdiran dongu
txt_files = [x for x in os.listdir(".") if x.endswith(".txt")]
for file_name in txt_files:
    uniqlines = set(open(file_name).readlines())
    bar = open(file_name, 'w').writelines(uniqlines)

#1 satir olan txt'leri no_need klasorune tasiyan dongu
txt_files = [x for x in os.listdir(".") if x.endswith(".txt")]
for file_name in txt_files:
    with open(file_name, 'r') as fp:
        x = len(fp.readlines())
        #print("file name: ", file_name, "Total lines: ", x)
        if(x == 1):
            #print("cagri name : " + file_name)
            new_path = path_no_need + "/" + file_name
            shutil.move(file_name, new_path)

pl = open('pureList', 'r')
for line in pl:
    pure_list.append(line)

#print("her itemdan 1 tane olan liste yazdiriliyor...")
#pure_list = sorted(pure_list)
#for item in pure_list:
    #print(item)

#print(len(pure_list))

item_count = len(pure_list)

#pure_list uzunlugunda n*n matris olustur
import numpy as np
np.set_printoptions(threshold=np.inf)
commit_matrix = np.zeros((item_count,item_count), dtype=np.int8)
commit_matrix_excel = np.chararray((item_count+1, item_count+2), itemsize = 50, unicode=True)
commit_matrix_excel[:] = ''

#kodun calistigi dizinde txt ile biten tum dosyalari al
txt_files = [x for x in os.listdir(".") if x.endswith(".txt")]

#tum txt'lerde pure_list'ten itemlari bulduktan sonra her bir dosya icin bulunan pure_list itemlari icin dosyayi tekrar acip diger itemlari kontrol eder
#eger diger itemlardan herhangi biri pure_listten ise matrisin ilgili indexini 1 arttir
for file_name in txt_files:
    with open(file_name, 'r') as fp:
       line = fp.readline()
       while line:
           for item in pure_list:
               #print("line: -" + line + "-")
               #print("item: -" + item + "-")
               #print("-----------")
               #print(line.startswith(item[:-1]))
               if(line.startswith(item[:-1])):
                   #print(item[:-1] + " found in " + line[:-1] + " in file -> " + file_name)
                   #print("first index: " + str(pure_list.index(item)))
                   with open(file_name, 'r') as fp_inside:
                       line_inside = fp_inside.readline()
                       while line_inside:
                           #print("line inside: "+line_inside)
                           for item_inside in pure_list:
                               #print("item_inside: "+item_inside)
                               #print(line_inside.startswith(item_inside[:-1]))
                               if(line_inside.startswith(item_inside[:-1]) and item_inside != item):
                                   #print("first index: " + str(pure_list.index(item)+1) + " calls " + "index inside: " + str(pure_list.index(item_inside)+1))
                                   #print(item[:-1] + " calls " + item_inside[:-1])
                                   commit_matrix[pure_list.index(item)][pure_list.index(item_inside)] += 1
                           line_inside = fp_inside.readline()
           line = fp.readline()

#print(commit_matrix)

#tek excel için doldurmaya başla

for x in range(item_count):
    for y in range(item_count):
        commit_matrix_excel[x+1][y+1] = commit_matrix[x][y]

for pure_item in pure_list:
    commit_matrix_excel[0][pure_list.index(pure_item)+1] = ''
    commit_matrix_excel[pure_list.index(pure_item)+1][0] = ''
    #commit_matrix_excel[pure_list.index(pure_item)+1][item_count+1] = pure_item
    #commit_matrix_excel[pure_list.index(pure_item)+2][0] = pure_item

commit_matrix_excel[0][0] = ''

#matrisi commit_counts.csv dosyasina yazar
np.savetxt("commit_counts.csv", commit_matrix_excel, delimiter=",", fmt='%s')
np.savetxt("commit_matrix.csv", commit_matrix, delimiter=",", fmt='%s')
#print(commit_matrix_excel)

print(str(args.p) + "'den fazla beraber commitlenen classlar yazdiriliyor...")
for x in range(item_count):
    for y in range(item_count):
        if(commit_matrix[x][y] > (args.p)):
            print("-> " + str(commit_matrix[x][y]) + " kere:")
            x_item = pure_list[x]
            y_item = pure_list[y]
            print("* " + x_item[:-1] + " - " + y_item[:-1])
            commit_together = (x_item[:-1], y_item[:-1])
            commit_list.append(commit_together)
            print("---")

#commit_list listeyi commit_together_list isimli dosyaya yaz
with open('commit_together_list', 'w+') as f:
    for item_commit in commit_list:
        f.writelines(item_commit[0] + "-" + item_commit[1] + "\n")