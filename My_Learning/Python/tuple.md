TODO: to be organised but things i've learnt  
credit to: https://pynative.com/python-tuple-exercise-with-solutions/


### removing duplicates from immutable (but want to preserve prev order):

```
from collections import OrderedDict
my_tuple = (1, 4, 2, 4, 2, 3, 5)
unique_ordered_tuple = tuple(OrderedDict.fromkeys(my_tuple))
```
<br><br>

### filtering from list
i solved the qn, but my ans was slightly diff

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
in this case, the variable `name` wasnt used on its own (eg to perform an operation), so instead i could have just referenced it (like shown in the ans)
<br><br>


### Map Tuples (where in the new tuple each num is ^2)

mine:
```
t = (1, 2, 3, 4)
print(f"Original tuple: {t}")
def squaring_tuple(num):
    return num**2

new_tuple = tuple(map(squaring_tuple, t))

print(f"answer: {new_tuple}")
```

answer given:  
Method 1: Using map() and tuple()
```
t = (1, 2, 3, 4)
print(f"Original tuple: {t}")

squared_tuple_map = tuple(map(lambda x: x**2, t))
print(f"Squared tuple (map function): {squared_tuple_map}")
```

Method 2: Using a loop
```
t = (1, 2, 3, 4)
print(f"Original tuple: {t}")

squared_list_loop = []
for num in t:
  squared_list_loop.append(num ** 2)
  squared_tuple_loop = tuple(squared_list_loop)
print(f"Squared tuple (loop): {squared_tuple_loop}")
```

i think my way of doing was technically mtd 1, but lamba might be more efficient since the named functions are already defined.  
looking at the lamba version made me think of using list comprehension:
```
squared_tuple = tuple(x**2 for x in t)
```

but would need to test to be sure whihc is most efficient
<br><br>


