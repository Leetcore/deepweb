#!/bin/bash
# Beispiel: ./take_screenshot.sh input.txt IndexOf
#
# Erstellt die Dateien "screenshots/IndexOf/2.56.98.169.jpeg" usw.
#

input_file=$1
output_dir=./screenshots/$2

if [ -d "$output_dir" ] 
then 
  echo "$output_dir is already existing"
else 
  mkdir -p ./screenshots/$2
fi

while IFS= read -r line; do

  
  index=$(echo $line | cut -d ',' -f 1)  
  # Ergibt: https://2.56.98.169/
  
  output_file=$(echo $line | cut -d '/' -f 1,2,3 | cut -d '/' -f 3)
  # Ergibt: 2.56.98.169

  output_path=$output_dir/$output_file.jpeg
  # Ergibt: ./screenshots/


  if [[ -f "$output_path" ]]  
  then
    echo "Screenshot of $index already exists. Skipping ..."
    
  else
    
    node ./take_screenshot.js --width=1280 --height=720 --outputDir=$output_dir --filename=$output_file --format=jpeg $index
    echo "Screenshot of $index was created"
    echo "Screenshot of $index was created" >> screenshot.log
  fi
  
  

done < $input_file
