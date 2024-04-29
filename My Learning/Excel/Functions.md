# Intro
These are the Excel functions taught and used in O Levels Computing

# Contents
- [Logical Functions](#logical)
- [Text Functions](#text)
- [Lookup Functions](#lookup)
- [Math Functions](#math)
- [Logical Functions](#logical)

Do note that the params in **bold** are compulsory for the functions below. If none are bolded, all params are needed for it to work as expected.

<a name="logical"></a>
## Logical Functions

| Operators | Meaning |
| - | - |
| < | Less than |
| <= | Less than or equal to |
| > | Greater than |
| >= | Greater than or equal to |
| = | Equal to |
| <> | Not equal to |
<br>


| Function | Syntax | Description | Fun Fact |
| - | - | - | - |
| IF | =IF(condition, value_if_true, value_if_false) | Returns _value_if_true_ when _condition_ is TRUE and _value_if_false_ when _condition_ is FALSE. | If =IF(condition, value_if_true), then if _condition_ is FALSE, returns FALSE. If =IF(condition,, value_if_false), then if _condition_ is TRUE, returns 0. |
| AND | =AND(**bool1**, bool2, ...) | Returns TRUE when all of the conditions in the cells are TRUE. Otherwise, returns FALSE. |
| OR | =OR(**bool1**, bool2, ...) | Returns TRUE when any of the conditions in the cells are TRUE. Otherwise, returns FALSE. |
| NOT | =NOT(bool) | Returns TRUE when _bool_ is FALSE, and FALSE when _bool_ is TRUE. |
<br>

<a name="text"></a>
## Text Functions
| Function | Syntax | Description | Fun Fact |
| - | - | - | - |
| LEN | =LEN(text) | Returns the number of characters in _text_. | 
| MID | =MID(text, start_num, num_of_char) | Returns _num_of_char_ characters starting from position _start_num_ of _text_. | 
| LEFT | =LEFT(**text**, num_of_char) | Returns _num_of_char_ characters from the beginning of _text_. | If _num_of_char_ is not stated, the function only returns the first character of _text_. |
| RIGHT | =RIGHT(**text**, num_of_char) | Returns _num_of_char_ characters from the end of _text_. | If _num_of_char_ is not stated, the function only returns the last character of _text_. |


<a name="lookup"></a>
## Lookup Functions
| Function | Syntax | Description | Fun Fact |
| VLOOKUP | =VLOOKUP(**lookup_value**, **table_range**, **col_index_num**, range_lookup) | It looks for _lookup_value_ in the first column of _table_range_ and returns the value from column _col_index_num_ in the row of _lookup_value_. <br /> If _range_lookup_ is TRUE, the function does an approximate match. <br /> If _range_lookup_ is not stated, the function does an exact match. <br /> If _range_lookup_ is not stated, the function does an approximate match. | Approximate match is what is "greater" than the value in the table. Eg if there are values 1, 5, 9, etc, lookup value of 9 would find in the 2nd row. 8 is closer to 9 numerically, but is less than 9 so it would search in the 2nd row (first value 5). If there is a value AB in the first column, a lookup value of "A", would not search in that row. But a lookup value of "abc" would return the value in that row of the stated column. |
| HLOOKUP | =HLOOKUP(**lookup_value**, **table_range**, **row_index_num**, range_lookup) |  |


SUM 
SUMIF
ROUND
RAND
RANDBETWEEN

<a name="math"></a>
## Math Functions
CEILING
FLOOR
POWER
SQRT

<a name="history"></a>
## 
COUNT
COUNTIF
COUNTA
COUNTBLANK

MIN
MAX
SMALL
LARGE

<a name="history"></a>
## Functions
PV
FV
RATE
PMT
IPMT
PPMT

<a name="misc"></a>
## Miscellaneous Functions 
| Function | Syntax | Description |
| - | - | - |
| TODAY | =TODAY() | Returns today's date. |

