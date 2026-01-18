### to be organised but things i've learnt


if you need to remove duplicates (but want to preserve prev order):

```
from collections import OrderedDict
my_tuple = (1, 4, 2, 4, 2, 3, 5)
unique_ordered_tuple = tuple(OrderedDict.fromkeys(my_tuple))
```
<br><br>
filtering from list

so i solved the qn, but my ans was slightly diff

mine:
```
students = [('Alice', 85), ('Bob', 92), ('Charlie', 78), ('David', 95)]
a_students = []

for name, score in students:
    if score >= 90:
        a_students += (name, score)

print(f"Students with scores 90 or above: {a_students}")
```

ans given:
```
students = [('Alice', 85), ('Bob', 92), ('Charlie', 78), ('David', 95)]
print(f"Original student list: {students}")

high_achievers_loop = []
for student in students:
  if student[1] >= 90:
    high_achievers_loop.append(student)
print(f"Students with scores 90 or above (loop method): {high_achievers_loop}")
```
so i thought abt why this was the model, and rmb that in clean code: keep it simple. should not initalise more than you need
in this case, the variable 'name' wasnt used on its own (eg to perform an operation), so instead i could have just referenced it (like shown in the ans)
