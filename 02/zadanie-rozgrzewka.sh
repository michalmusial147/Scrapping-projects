curl -s  "https://p.lodz.pl/" | tr '"' '\n' | tr "'" '\n' | grep -e '^https://' -e '^http://' -e'^//' | sort
"wc" do policzenia wszystkich wpisów
"uniq -c" do policzenia wystąpień
curl -s  "https://p.lodz.pl/" | tr '"' '\n' | tr "'" '\n' | grep -e '^https://' -e '^http://' -e'^//' | sort | uniq -c | grep --color  -E 'azs|rds|bon|$'
