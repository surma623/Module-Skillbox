import re

text = 'Even if they are djinns, I will get djinns that can outdjinn them.'

pattern = r'\b[aeiouAEIOU]\w*'

result = re.findall(pattern, text)

print(result)

pattern = r'\b[^aeiouAEIOU\W]\w*'

result = re.findall(pattern, text)

print(result)
