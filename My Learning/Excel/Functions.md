# Intro
These are the Excel functions taught and used in O Levels Computing

# Contents
- [Logical Functions](#logical)
- [Text Functions](#text)
- [Lookup Functions](#lookup)
- [Math Functions](#math)
- [Logical Functions](#logical)



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

Do note that the params in **bold** are compulsory for the functions below. If none are bolded, all params are needed for it to work as expected.
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
| LEFT | =LEFT(**text**, num_of_char) | Returns _num_of_char_ characters from the beginning of _text_. | If _num_of_char_ is not stated, the function only returns the first character of _text_.
| RIGHT | =RIGHT(**text**, num_of_char) | Returns _num_of_char_ characters starting from position _start_num_ of _text_. | 


<a name="lookup"></a>
## Lookup Functions
VLOOKUP
HLOOKUP

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

