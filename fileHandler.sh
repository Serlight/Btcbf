#!/bin/bash
  
input_file="/Users/hcc/python/Btcbf/wallets/splitaddress00"  # 输入文件名  
output_file="/Users/hcc/python/Btcbf/wallets/splitadress00_nb.txt"  # 输出文件名  
  
if [ ! -f "$input_file" ]; then  
  echo "输入文件不存在！"  
  exit 1  
fi  
  
mapfile -t lines < "$input_file"  # 读取文件内容到数组  
  
> "$output_file"  # 清空输出文件  
  
for line in "${lines[@]}"; do  
  first_word=$(echo "$line" | cut -d "	" -f 1)  # 使用空格作为分隔符，获取第一个元素 
  echo "$first_word" >> "$output_file"  # 将第一个元素追加到输出文件  
done  
  
echo "完成！"