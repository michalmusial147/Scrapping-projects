import re

row = "7Łódź92-014PolandŁódź VoivodeshipLodzŁódź\xa0\xa0\xa0+90.0/-127.55433"
pattern = re.compile(r"[0-9]{2}-[0-9]{3}")
res = pattern.search(row)
print(res)
