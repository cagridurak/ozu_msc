#!/usr/bin/python

import os;
import numpy as np
np.set_printoptions(threshold=np.inf)

import argparse
parser = argparse.ArgumentParser(description='dependency finder arguments')
parser.add_argument("-p", type=int, required=True, help="kactan fazla dependenti olan classlar yazdirilsin?")
parser.add_argument("-d", type=int, required=True, help="kactan fazla classa dependent olan classlar yazdirilsin?")
args = parser.parse_args()

#print('args.p:', args.p)
#print('args.d:', args.d)

pure_list = []
contains = 0
dep_gecici = []
cycle_matrix = []

#kodun calistirildigi dizinde cpp ve hpp ile biten tum dosyalari bul
cpp_hpp_files = [x for x in os.listdir(".") if x.endswith(".cpp") or x.endswith(".hpp")]

#bulunan tum dosyalari .cpp ve .hpp son eklerini cikararak bir listeye ekle
for file_name in cpp_hpp_files:
    #print(file_name)
    #file_name = file_name[:-4]
    pure_name = file_name[:-4]
    pure_list.append(pure_name)
    #print(file_name)

#txtlerde ayni isimli classlardan 1 tane yazdiran dongu
pure_list = list(dict.fromkeys(pure_list))
pure_list = sorted(pure_list)

#print("her itemdan 1 tane olan liste yazdiriliyor...")
#print(pure_list)
#print(len(pure_list))

#unique isimlerin oldugu listeyi pureList isimli dosyaya yaz
with open('pureList', 'w+') as f:
    for item in pure_list:
        f.write("%s\n" % item)


#pure_list uzunlugunda n*n matris yarat ve sifirlar ile doldur
item_count = len(pure_list)
dependency_matrix = np.zeros((item_count,item_count), dtype=np.int8)
dependency_matrix_excel = np.chararray((item_count+1, item_count+1), itemsize = 50, unicode=True)
dependency_matrix_excel[:] = ''
#include ile baslayan tum satirlarda purelist'i ara ve dep_gecici matrisini doldur
cpp_hpp_files = [x for x in os.listdir(".") if x.endswith(".cpp") or x.endswith(".hpp")]
for file_name in cpp_hpp_files:
    length_of_filename = len(file_name)
    with open(file_name) as fp:
       line = fp.readline()
       while line:
           if(line.startswith('#include')):
               #print(line)
               for pure_item in pure_list:
                   #print("item_say " + pure_item)
                   if pure_item in line:
                       #print("item_say " + pure_item)
                       #print(line)
                       cut_line = line[10:]
                       #print("karsilastir 1 "+cut_line[:length_of_filename])
                       #print("karsilastir 2 "+file_name)
                       cpp_hali = file_name[:-4] + ".cpp";
                       hpp_hali = file_name[:-4] + ".hpp";
                       if(hpp_hali != cut_line[:length_of_filename] and cpp_hali != cut_line[:length_of_filename]):
                           #print("first index: " + str(pure_list.index(file_name[:-4])+1))
                           #print("second index: " + str(pure_list.index(pure_item)+1))
                           #dependency_matrix[pure_list.index(file_name[:-4])][pure_list.index(pure_item)] = 1
                           #print("in file " + file_name)
                           #print(file_name[:-4] + " -> " + line[10:-6])
                           item_gecici = (file_name[:-4], line[10:-6])
                           dep_gecici.append(item_gecici)
           line = fp.readline()


#dep_gecici matrisinde duplicate itemlari cikar
dep_gecici = list(dict.fromkeys(dep_gecici))
dep_gecici = sorted(dep_gecici)
#print("dep gecici yazdiriliyor...")
#print(dep_gecici)

#tum dependency'leri yazdir
print("dependencies:")
print("----")
for dep_item in dep_gecici:
    print("-> " + dep_item[0] + " is dependent on " + dep_item[1])
    print("----")
    dependency_matrix[pure_list.index(dep_item[0])][pure_list.index(dep_item[1])] = 1

print("----------")

print("sum of rows:")
print(np.sum(dependency_matrix,axis=1).tolist())
row_list = np.sum(dependency_matrix,axis=1).tolist()
print("----------")
print("sum of columns:")
column_list = np.sum(dependency_matrix,axis=0).tolist()
print(np.sum(dependency_matrix,axis=0).tolist())
print("----------")
print("\n")
print("********************")
counter = 0

print(str(args.p) + "'den fazla dependent'i olan classlar yazdiriliyor...")
print("(unstable interface)")
print("-----------------------")
for column_item in column_list:
    counter +=1
    if (column_item > args.p):
        print("--> " + pure_list[counter-1])
print("********************")
print("\n")
print("********************")
counter = 0
print(str(args.d) + "'den fazla class'a dependent olan classlar yazdiriliyor...")
print("-----------------------")
for row_item in row_list:
    counter +=1
    if (row_item > args.d):
        print("--> " + pure_list[counter-1])
print("********************")
print("\n")
print("********************")
print("A->B->A tipi cyclic dependency olan classlar yazdiriliyor...")
print("---")
q = 0
w = 0
for dep_item in dep_gecici:
    q+=1
    for dep_reverse in dep_gecici:
        w+=1
        if(dep_item[0] == dep_reverse[1]):
            if(dep_item[1] == dep_reverse[0]):
                item_gecici = (pure_list.index(dep_item[0]), pure_list.index(dep_item[1]))
                cycle_matrix.append(item_gecici)
                print("--> cyclic dep: " + dep_item[0] + " and " + dep_item[1])
                print("")
print("********************")
print("\n\n")
print("********************")

print("A->B->C->A tipi cyclic dependency olan classlar yazdiriliyor...")
print("---")
for first_cycle in dep_gecici:
    #print("first_cycle[0]: " + first_cycle[0] + " - first_cycle[1]:" + first_cycle[1])
    for second_cycle in dep_gecici:
        #print("second_cycle[0]: " + second_cycle[0] + " - second_cycle[1]:" + second_cycle[1])
        for third_cycle in dep_gecici:
            #print("third_cycle[0]: " + third_cycle[0] + " - third_cycle[1]:" + third_cycle[1])
            #print(first_cycle[0] + " - " + second_cycle[1])
            if(first_cycle[0] == second_cycle[1]):
                if(second_cycle[0] == third_cycle[1]):
                    if(third_cycle[0] == first_cycle[1]):
                        print("--> cyclic dep: " + first_cycle[0] + " is dependent on " + first_cycle[1] + ", AND " + first_cycle[1] + " is dependent on " + third_cycle[1])
                        print("")
print("********************")
print("\n\n")
print("********************")

print("A->B->C->D->A tipi cyclic dependency olan classlar yazdiriliyor...")
print("---")
for first_cycle in dep_gecici:
    for second_cycle in dep_gecici:
        for third_cycle in dep_gecici:
            for fourth_cycle in dep_gecici:
                if(first_cycle[0] == second_cycle[1]):
                    if(second_cycle[0] == third_cycle[1]):
                        if(third_cycle[0] == fourth_cycle[1]):
                            if(fourth_cycle[0] == first_cycle[1]):
                                print("--> cyclic dep: " + first_cycle[0] + " is dependent on " + first_cycle[1] + ", " + first_cycle[1] + " is dependent on " + third_cycle[0] + ", " + third_cycle[0] + " is dependent on " + third_cycle[1] + " AND " + third_cycle[1] + " is dependent on " + first_cycle[0])
                                print("")
print("********************")
print("\n\n")

#tek excel için doldurmaya başla
for pure_item in pure_list:
    if column_list[pure_list.index(pure_item)] > args.p:
        dependency_matrix_excel[0][pure_list.index(pure_item)+1] = str((pure_list.index(pure_item)+1)) + ' (uns if)'
    else:
        dependency_matrix_excel[0][pure_list.index(pure_item)+1] = (pure_list.index(pure_item)+1)
    dependency_matrix_excel[pure_list.index(pure_item)+1][0] = pure_item
    dependency_matrix_excel[0][0] = ''

#tek excel için DP'leri yaz
for dep_item in dep_gecici:
    dependency_matrix_excel[pure_list.index(dep_item[0])+1][pure_list.index(dep_item[1])+1] = 'Dp'

#print(dependency_matrix_excel)

for cycle_item in cycle_matrix:
    dependency_matrix_excel[cycle_item[0]+1][cycle_item[1]+1] += ('-cyclic:' + pure_list[cycle_item[1]])
    

np.savetxt("dependency_matrix.csv", dependency_matrix_excel, delimiter=",", fmt='%s')