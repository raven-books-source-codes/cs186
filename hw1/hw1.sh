#!/bin/bash
# bash command-line arguments are accessible as $0 (the bash script), $1, etc.
# echo "Running" $0 "on" $1

# Step1: gnereate ebook.csv from argv
python3 txt2csv.py $1

# Step2: generate tokens.csv
python3 csv2token.py

# Step3: generate token_counts.csv from tokens.csv
echo "token,count" > token_counts.csv
tail -n +2 tokens.csv | cut -d ',' -f 2 | sort | uniq -c | sed 's/^ *//g' | awk -v RS='\r\n'  '{print $2,$1}' OFS=',' ORS='\r\n' >> token_counts.csv 

# Step4: generate token_counts.csv from tokens.csv
echo "token,count" > name_counts.csv
for line in $(cat popular_names.txt)
do
	grep -iw $line token_counts.csv >> name_counts.csv
done


exit 0