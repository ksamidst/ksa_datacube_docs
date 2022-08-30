#!/bin/sh
echo "Enter input directories path:>>"
read input_dir_path
echo "Enter output yamls directories path:>>"
read output_yaml_path

count = 0

for dir in $input_dir_path/*
do
  echo $dir
  #echo $output_yaml_path
  #echo $count
  #echo scene$count.odc-metadata.yaml
  python /root/scripts/prep_ls8_sr.py $dir $output_yaml_path $count
  datacube dataset add $output_yaml_path/scene$count.odc-metadata.yaml
  ((count=count+1))
done
