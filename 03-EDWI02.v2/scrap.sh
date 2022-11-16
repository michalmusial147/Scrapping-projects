!/bin/bash

starting_code=62000
ending_code=99999
base_url="https://www.geonames.org/postalcode-search.html?country=PL&q="
fetched_site_file="./website.html"
row_file="./row.txt"

for i in $(seq -f "%05g" "$starting_code" "$ending_code"); do
  post_code="${i:0:2}-${i:2:6}"
  wget -O $fetched_site_file "$base_url$post_code"
  line_number=1
  restable_line_number=-1
  while read -r line
  do
    if [[ $line == *restable* ]]; then
      restable_line_number=${line_number}
    elif (( $line_number == ($restable_line_number + 2) )); then
      echo "$line" >> $row_file
      city=$(xmllint --html --xpath "string(//tr[1]/td[2])" $row_file)
      post_code=$(xmllint --html --xpath "string(//tr[1]/td[3])" $row_file)
      country=$(xmllint --html --xpath "string(//tr[1]/td[4])" $row_file)
      admin1=$(xmllint --html --xpath "string(//tr[1]/td[5])" $row_file)
      admin2=$(xmllint --html --xpath "string(//tr[1]/td[6])" $row_file)
      admin3=$(xmllint --html --xpath "string(//tr[1]/td[7])" $row_file)
      cords=$(xmllint --html --xpath "string(//tr[2]/td[2]/a/small)" $row_file)
      echo "${city},${post_code},${country},${admin1},${admin1},${admin2},${admin3}" >> "result_by_bash.csv"
      break
	fi
	let line_number=${line_number}+1
  done < $fetched_site_file
  rm -f $row_file
done
