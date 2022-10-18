#!/bin/sh

rm -rf diffs
rm -rf dependency_matrix.csv
rm -rf pureList
rm -rf commit_counts.csv
rm -rf merge.csv

echo "kactan fazla dependenti olan classlar yazdirilsin? (Unstable Interface)"
read var1
echo "kactan fazla classa dependent olan classlar yazdirilsin?"
read var2

python3 dependencyFinder.py -p $var1 -d $var2
echo "dependecy bulma islemi bitti!"
echo -e "-------------------\n\n\n"


mkdir diffs

svn log | grep -e "lines" | cut -d " " -f 1 | cut -c 2- | grep -Eo '[0-9]{0,9}' > diffs/revisions.txt

while read i ; do echo "$i"; j=$((i-1)); svn diff -r $j:$i --summarize > diffs/$i.txt; done < diffs/revisions.txt

cp -f relationWorks.py relationFinder.py
mv -f relationFinder.py diffs
cp -f pureList diffs/

cd diffs
rm -f commit_together_list

echo "class iliskilerini bulma islemi basliyor..."
echo "kactan fazla beraber commitlenen classlar yazdirilsin?"
read var3
python3 relationFinder.py -p $var3

cd ..
cp -f diffs/commit_counts.csv .

python3 mergeOperations.py -p $var3