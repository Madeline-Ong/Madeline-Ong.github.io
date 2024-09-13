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
{<i>variable</i>:><i>n</i>}

<br>

With leading 0s
{<i>variable</i>:0<i>n</i>}
<br>


zfill
rjust
<br><br>


Tenary Operator
One-liner if-else but the expanded is more efficient
<br>


List Comprehension
Quick way to produce list w/o needing to initalise -> less memory used
Base eg:
\[<i>expression</i> for <i>element</i> in <i>iterable</i>]
<br>

With If
\[<i>expression_if_true</i> for <i>element</i> in <i>iterable</i> <i>condition</i>]
<br>

With If-Else
\[<i>expression_if_true</i> if <i>condition</i> <i>expression_if_false</i> for <i>element</i> in <i>iterable</i>]
<br>
<br>


Dictionary Comprehensions
base case: {<i>key_expression</i>: <i>value_expression</i> for <i>element</i> in <i>iterable</i>}
Note: The for_loop either contains 1 element that is passed in and used for both key & value, or 2 elements
<br>

1 element:
{<i>key_expression</i>: <i>value_expression</i> for <i>element</i> in <i>iterable</i>}
num_list = [1,2,3]
{x: x*2 for x in num_list}
<br>

2 elements
{<i>key_expression</i>: <i>value_expression</i> for <i>elements</i> in <i>iterables</i>}
{key: val for (key, val) in zip(keys, values)}
<br>

Can also use with If-Else
With If
{<i>key_expression</i>: <i>value_expression</i> for <i>element</i> in <i>iterable</i> if <i>condition</i>}
<br>

With If-Else (can be applied for key expression as well, eg just shows for value)
{<i>key_expression</i>: (<i>value_expression_if_true</i> if <i>condition</i> <i>value_expression_if_false</i>)  for <i>element</i> in <i>iterable</i> if <i>condition</i>}

<br>
<br>


