# Intro
Taking O Levels Computing exposed me to functions that can be used in Excel for data entry.
Subsequently, I have also learnt new functions (at my internship, etc), which will be added.

Note that the params in **bold** are compulsory for the functions below. If none are bolded, all params are needed so that it will work as expected.

# Contents
- [Logical Functions](#logical)
- [Text Functions](#text)
- [Lookup Functions](#lookup)
- [Math Functions](#math)
- [Statistical Functions](#stat)
- [Financial Functions](#financial)
- [Miscellaneous Functions](#misc)
- [To Be Added](#more)

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

For both functions stated below, there is a parameter: <i>range_lookup</i>, which is optional and takes the values TRUE or FALSE.
If <i>range_lookup</i> is TRUE, the function does an approximate match.
If <i>range_lookup</i> is FALSE, the function does an exact match.
If <i>range_lookup</i> is not stated, the function does an approximate match.

An approximate match is when the function finds what value in the table the <i>lookup_value</i> is "greater" than.
If there are values 1, 5, 9, etc in the first row/column, with a lookup value of 8, the function would look in the 2nd column/row. 8 is closer to 9 numerically, but is less than 9 and greater than 5, so it would search in the 2nd column/row (first value 5).
If there is a value AB in the first row/column, with a lookup value of "A", the function would not look into that column/row. But with a lookup value of "abc", the function would return the value in that column/row of the stated row/column.

<table>
  <tr>
    <th>Function</th>
    <th>Syntax</th>
    <th>Description</th>
    <th>More Info</th>
  </tr>
  <tr>
    <td>HLOOKUP</td>
    <td>=HLOOKUP(<b>lookup_value</b>, <b>table_range</b>, <b>row_index_num</b>, range_lookup)</td>
    <td>It looks for <i>lookup_value</i> in the first row of <i>table_range</i> and returns the value from row <i>row_index_num</i> in the column of <i>lookup_value</i>.</td>
    <td></td>
  </tr>
  <tr>
    <td>VLOOKUP</td>
    <td>=VLOOKUP(<b>lookup_value</b>, <b>table_range</b>, <b>col_index_num</b>, range_lookup)</td>
    <td>It looks for <i>lookup_value</i> in the first column of <i>table_range</i> and returns the value from column <i>col_index_num</i> in the row of <i>lookup_value</i>.<br><br>
    <td></td>
  </tr>
</table>


<a name="math"></a>
## Math Functions
<table>
  <tr>
    <th>Function</th>
    <th>Syntax</th>
    <th>Description</th>
    <th>More Info</th>
  </tr>
  <tr>
    <td>CEILING</td>
    <td>=CEILING(number, significance)</td>
    <td>Returns <i>number</i> rounded <strong>up</strong> to a multiple of <i>significance</i>.<br><br>
    Eg: =CEILING(10.123, 0.03) returns 10.14, which is a multiple of 0.03. 
    </td>
    <td></td>
  </tr>
  <tr>
    <td>FLOOR</td>
    <td>=FLOOR(number, significance)</td>
    <td>Returns <i>number</i> rounded <strong>down</strong> to a multiple of <i>significance</i>.<br><br>
    Eg: =CEILING(10.123, 0.03) returns 10.11, which is a multiple of 0.03. 
    <td></td>
  </tr>
  <tr>
    <td>POWER</td>
    <td>=POWER(number, power)</td>
    <td>Returns <i>number</i> raised to the exponent <i>power</i>.</td>
    <td></td>
  </tr>
  <tr>
    <td>SQRT</td>
    <td>=SQRT(number)</td>
    <td>Returns the square root of <i>number</i></td>
    <td></td>
  </tr>
  <tr>
    <td>ROUND</td>
    <td>=ROUND(number, num_of_digits)</td>
    <td>Returns <i>number</i> rounded to <i>num_of_digits</i> decimal place(s).<br><br>
    Eg: =ROUND(10.123, 0) returns 10.<br><br> =ROUND(10.123, 2) returns 10.12.</td>
    <td></td>
  </tr>
  <tr>
    <td>RAND</td>
    <td>=RAND()</td>
    <td>Returns a random number greater than or equal to 0 and less than 1.</td>
    <td></td>
  </tr>
  <tr>
    <td>RANDBETWEEN</td>
    <td>=RANDBETWEEN(lowest, highest)</td>
    <td>Returns a random number between the whole numbers <i>lowest</i> and <i>highest</i> (inclusive of both).</td>
    <td></td>
  </tr>
  <tr>
    <td>SUM</td>
    <td>=SUM(<b>num1</b>, num2, ...)</td>
    <td>Returns the total of the stated numbers or numbers in the cell range.</td>
    <td></td>
  </tr>
  <tr>
    <td>SUMIF</td>
    <td>=SUMIF(<b>range</b>, <b>condition</b>, sum_range)</td>
    <td>Returns the sum of the numbers in <i>sum_range</i> where the corresponding value in <i>range</i> satisfies <i>condition</i>.</td>
    <td>If <i>sum_range</i> is not stated, then <i>range</i> is used as <i>sum_range</i>.</td>
  </tr>
  <tr>
    <td>MOD</td>
    <td>=MOD(number, divisor)</td>
    <td>Returns the remainder when <i>number</i> is divided by <i>divisor</i>.</td>
    <td></td>
  </tr>
</table>


<a name="stat"></a>
## Statistical Functions
<table>
  <tr>
    <th>Function</th>
    <th>Syntax</th>
    <th>Description</th>
    <th>More Info</th>
  </tr>
  <tr>
    <td>MAX</td>
    <td>=MAX(<b>num1</b>, num2, ...)</td>
    <td>Returns the largest number out of the stated numbers or the numbers in the cell range.</td>
    <td></td>
  </tr>
  <tr>
    <td>MIN</td>
    <td>=MIN(<b>num1</b>, num2, ...)</td>
    <td>Returns the smallest number out of the stated numbers or the numbers in the cell range.</td>
    <td></td>
  </tr>
  <tr>
    <td>SMALL</td>
    <td>=SMALL(range, k)</td>
    <td>Returns the <i>k</i>th smallest number in <i>range</i>.</td>
    <td></td>
  </tr>
  <tr>
    <td>LARGE</td>
    <td>=LARGE(range, k)</td>
    <td>Returns the <i>k</i>th largest number in <i>range</i>.</td>
    <td></td>
  </tr>
  <tr>
    <td>MODE.SNGL</td>
    <td>=MODE.SNGL(<b>num1</b>, num2, ...)</td>
    <td>Returns the most frequently occurring value of the stated numbers or the numbers in cell range.</td>
    <td></td>
  </tr>
  <tr>
    <td>MEDIAN</td>
    <td>=MEDIAN(<b>num1</b>, num2, ...)</td>
    <td>Returns the middle number of the stated numbers or the numbers in cell range.</td>
    <td></td>
  </tr>
  <tr>
    <td>AVERAGE</td>
    <td>=AVERAGE(<b>num1</b>, num2, ...)</td>
    <td>Returns the mean of the stated numbers or the numbers in cell range.</td>
    <td></td>
  </tr>
  <tr>
    <td>PERCENTILE</td>
    <td>=PERCENTILE(range, k)<br><br>
    Note that <i>k</i> should be between 0 and 1 (inclusive).</td>
    <td>Returns the (k × 100)th percentile of the numbers in range.
    Eg: =PERCENTILE(A1:A10, 0.2) returns the 20th percentile of A1:A10.</td>
    <td>If k is 0, then this function is equivalent to MIN().
If k is 0.5, then this function is equivalent to MEDIAN().
If k is 1, then this function is equivalent to MAX().</td>
  </tr>
  <tr>
    <td>QUARTILE</td>
    <td>=QUARTILE(range, quart)</td>
    <td>Returns a specified quartile of the numbers in <i>range</i>.</td>
    <td>
    If <i>quart</i> is 0, then the function returns the smallest number of <i>range</i> (same as MIN()).<br><br>
    If <i>quart</i> is 1, then the function returns the first quartile (25th percentile).<br><br>
    If <i>quart</i> is 2, then the function returns the middle number of <i>range</i> (same as MEDIAN().<br><br>
    If <i>quart</i> is 3, then the function returns the third quartile (75th percentile).<br><br>
    If <i>quart</i> is 4, then the function returns the largest number of <i>range</i> (same as MAX()).<br><br>
  </tr>
  <tr>
    <td>STDEV</td>
    <td>=STDEV(<b>num1</b>, num2, ...)</td>
    <td>Returns the standard deviation of the stated numbers or the numbers in cell range.</td>
    <td>Standard deviation is sqrt of variance <br><br>
    Formula: 
    </td>
  </tr>
  <tr>
    <td>VAR</td>
    <td>=VAR(<b>num1</b>, num2, ...)</td>
    <td>Returns the variance of the stated numbers or the numbers in cell range.</td>
    <td>Variance is the sq of standard deviation <br><br>
    Formula: 
    </td>
  </tr>
  <tr>
    <td>COUNT</td>
    <td>=COUNT(<b>range1</b>, range2, ...)</td>
    <td>Returns the number of cells that contains numbers, currencies, dates, times and percentages in the stated range reference(s).</td>
    <td>Empty cells and cells with text or bool values not counted.</td>
  </tr>
  <tr>
    <td>COUNTA</td>
    <td>=COUNTA(<b>range1</b>, range2, ...)</td>
    <td>Returns the number of non-empty cells in the stated cell reference(s). </td>
    <td>Empty cells are not counted, the function counts cells with any content.</td>
  </tr>
  <tr>
    <td>COUNTBLANK</td>
    <td>=COUNTBLANK(range)</td>
    <td>Returns the number of empty cells in <i>range</i>.</td>
    <td></td>
  </tr>
  <tr>
    <td>COUNTIF</td>
    <td>=COUNTIF(range, condition)</td>
    <td>Returns the number of cells in <i>range</i> that satisfies <i>condition</i>.</td>
    <td></td>
  </tr>
</table>

<a name="financial"></a>
## Financial Functions
Function params & their meaning:
- pv (present value): Cash flow of borrower when loan is made (always positive)
- fv (future value): Cash flow of borrower when loan ends (usually zero or negative)
- nper: Number of periods for length of loan
- rate: Interest rate per period (e.g., per month or per year)
- pmt: Payment per period (always negative for instalments)
There are arguments fixed at 0 because only lump sum payments are considered.

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

<a name="more"></a>
## To Be Added
FILTER
XLOOKUP


