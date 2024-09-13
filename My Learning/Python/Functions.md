This is a library of helpful functions, as well as a place to consolidate what I know.

The params in _italics_ are compulsory. 
| Function | Description | Syntax |
| - | - | - |
| count() | Counts the num of times a substring appears in the string. | string.count(_substring_, start, end) |
| encode() | Encodes strings with the specified encoding scheme. Default is UTF-8. | string.encode(_encoding_, errors) |
| endwith() | Returns true if the string ends with the specified substring. | string.endswith(_substring_, start, end) |
| find() | Finds the first occurrence of the substring and returns the index. Returns -1 if not found. | string.find(_substring_, start, end) |
| format() | Format the substring(s) into the string using the {} placeholder. (refer below for more formatting) | "string {}".format(_substring1_, substring2...) |
| index() | Finds the first occurrence of the substring and returns the index. Raises an exception if not found. | string.index(_substring_, start, end) |
| join() | - | - |
| replace() | - | - |
| startswith() | - | - |
| strip() | Trims the string | - |
| count() | - | - |

Format
| Format | Description | 
| - | - | 


f-strings

Formatting Strings
Paddings
With Space (n is number of space)
Right Align the element:
{variable:>n}

With leading 0s
{variable:0n}

zfill
rjust


Tenary Operator
One-liner if-else but the expanded is more efficient


List Comprehension
Quick way to produce list w/o needing to initalise -> less memory used
Base eg:
\[<i>expression</i> <i>for_loop</i>]

With If
\[<i>expression_if_true</i> <i>for_loop</i> <i>condition</i>]

With If-Else
\[<i>expression_if_true</i> <i>condition</i> <i>expression_if_false</i> <i>for_loop</i>]


Dictionary Comprehensions
base case: {key_expression: value_expression for ele in iterable}
Note: The for_loop either contains 1 element that is passed in and used for both key & value, or 2 elements

1 element:
num_list = [1,2,3]
{x: x*2 for x in num_list}

2 elements
{key: val for (key, val) in zip(keys, values)}

Can also use with If-Else
With If
{key_expression: value_expression for ele in iterable if condition}

With If-Else (can be applied for key expression as well, eg just shows for value)
{key_expression: (value_expression_if_true if condition value_expression_if_false)  for ele in iterable if condition}



