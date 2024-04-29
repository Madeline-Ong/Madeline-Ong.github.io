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

<table>
  <tr>
    <th>Operator</th>
    <th>Meaning</th>
  </tr>
  <tr>
    <td>&lt;</td>
    <td>Less than</td>
  </tr>
  <tr>
    <td>&lt;=</td>
    <td>Less than or equal to</td>
  </tr>
  <tr>
    <td>&gt;</td>
    <td>Greater than</td>
  </tr>
  <tr>
    <td>&gt;=</td>
    <td>Greater than or equal to</td>
  </tr>
  <tr>
    <td>=</td>
    <td>Equal to</td>
  </tr>
  <tr>
    <td>&lt;&gt;</td>
    <td>Not equal to</td>
  </tr>
</table>
<br>


<table>
  <tr>
    <th>Function</th>
    <th>Syntax</th>
    <th>Description</th>
    <th>More Info</th>
  </tr>
  <tr>
    <td>IF</td>
    <td>=IF(condition, value_if_true, value_if_false)</td>
    <td>Returns <i>value_if_true</i> when <i>condition</i> is TRUE and <i>value_if_false</i> when <i>condition</i> is FALSE.</td>
    <td>For =IF(condition, value_if_true), if <i>condition</i> is FALSE, returns FALSE. For =IF(condition,, value_if_false), if <i>condition</i> is TRUE, returns 0.</td>
  </tr>
  <tr>
    <td>AND</td>
    <td>=AND(<b>bool1</b>, bool2, ...)</td>
    <td>Returns TRUE when all of the conditions in the cells are TRUE. Otherwise, returns FALSE.</td>
    <td></td>
  </tr>
  <tr>
    <td>OR</td>
    <td>=OR(<b>bool1</b>, bool2, ...)</td>
    <td>Returns TRUE when any of the conditions in the cells are TRUE. Otherwise, returns FALSE.</td>
    <td></td>
  </tr>
  <tr>
    <td>NOT</td>
    <td>=NOT(bool)</td>
    <td>Returns TRUE when <i>bool</i> is FALSE, and FALSE when <i>bool</i> is TRUE.</td>
    <td></td>
  </tr>
</table>
<br>

<a name="text"></a>
## Text Functions
<table>
  <tr>
    <th>Function</th>
    <th>Syntax</th>
    <th>Description</th>
    <th>More Info</th>
  </tr>
  <tr>
    <td>LEN</td>
    <td>=LEN(text)</td>
    <td>Returns the number of characters in <i>text</i></td>
    <td></td>
  </tr>
  <tr>
    <td>MID</td>
    <td>=MID(text, start_num, num_of_char)</td>
    <td>Returns <i>num_of_char</i> characters starting from position <i>start_num</i> of <i>text</i>.</td>
    <td></td>
  </tr>
  <tr>
    <td>LEFT</td>
    <td>=LEFT(<b>text</b>, num_of_char)</td>
    <td>Returns <i>num_of_char</i> characters from the beginning of <i>text</i>.</td>
    <td>If <i>num_of_char</i> is not stated, the function only returns the first character of <i>text</i>.</td>
  </tr>
  <tr>
    <td>RIGHT</td>
    <td>=RIGHT(<b>text</b>, num_of_char)</td>
    <td>Returns <i>num_of_char</i> characters from the end of <i>text</i>.</td>
    <td>If <i>num_of_char</i> is not stated, the function only returns the last character of <i>text</i>.</td>
  </tr>
</table>

<a name="lookup"></a>
## Lookup Functions
<table>
  <tr>
    <th>Function</th>
    <th>Syntax</th>
    <th>Description</th>
    <th>More Info</th>
  </tr>
  <tr>
    <td>VLOOKUP</td>
    <td>=VLOOKUP(<b>lookup_value</b>, <b>table_range</b>, <b>col_index_num</b>, range_lookup)</td>
    <td>It looks for <i>lookup_value</i> in the first column of <i>table_range</i> and returns the value from column <i>col_index_num</i> in the row of <i>lookup_value</i>.<br><br>If <i>range_lookup</i> is TRUE, the function does an approximate match.<br><br> If <i>range_lookup</i> is not stated, the function does an exact match.<br><br> If <i>range_lookup</i> is not stated, the function does an approximate match.</td>
    <td>Approximate match is what is "greater" than the value in the table. Eg if there are values 1, 5, 9, etc, lookup value of 9 would find in the 2nd row. 8 is closer to 9 numerically, but is less than 9 so it would search in the 2nd row (first value 5). If there is a value AB in the first column, a lookup value of "A", would not search in that row. But a lookup value of "abc" would return the value in that row of the stated column.</td>
  </tr>
  <tr>
    <td>HLOOKUP</td>
    <td>=HLOOKUP(<b>lookup_value</b>, <b>table_range</b>, <b>row_index_num</b>, range_lookup)</td>
    <td>Less</td>
    <td>Less</td>
  </tr>
</table>

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

