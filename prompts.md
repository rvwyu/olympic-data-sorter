# Prompts log

This file logs the tool/prompts you used and the results. A small note on whether it was successful, choices you made and what was used.

## Group:

| AI tool name | prompt                                                                                           | result                                                     |
| ------------ | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| gh copilot   | what do you use to read in csv files in python                                                   | csv module or pandas, rejected pandas as it is not allowed |
| gh copilot   | write a function that is passed the name of a csv file and will return the data set of that file | read_csv_file(file_name)                                   |

## Sang Yu Lee:

| AI tool name | prompt                                                                                                                                                          | result                                                                                                              |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| ChatGPT      | How to solve the problem of circular import between two Python files? A file uses two functions which are declared in B file. B file uses a function in A file. | It suggested 4 ways to solve it. I chose the restructuring my code by adding another file to avoid circular import. |
| ChatGPT      | How can I loop through a list in Python with the index?                                                                                                         | It suggested the 'enumerate()' function.                                                                            |
| ChatGPT      | How to create a dictionary with specific elements in two-dimensional list                                                                                       | It suggested {item[0]: item[2] for item in data}                                                                    |
| ChatGPT      | How can I convert a boolean value to the string 'True' or 'False' in Python?                                                                                    | It suggested the function str().                                                                                    |
| ChatGPT      | How can I insert multiple value into a list at once?                                                                                                            | It suggested the function extend().                                                                                 |

## Hoang Phuc Huynh:

| AI tool name | prompt                                         | result                                                                        |
| ------------ | ---------------------------------------------- | ----------------------------------------------------------------------------- |
| ChatGPT      | How to slice list in Python                    | It suggests using the slice notation: list[start:stop:step]                   |
| ChatGPT      | How to join a list in Python                   | It suggests using join() method: separator.join(list)                         |
| ChatGPT      | How to generate a random number                | It suggests using random module                                               |
| ChatGPT      | How to find a character in a string            | It suggests using the find() method                                           |
| ChatGPT      | How to create a string from multiple variables | It suggests 4 ways to create and I chose using "f-strings" to create a string |

## Rhowen Vaughn Wendelle Yu:

| AI tool name | prompt | result |
| ------------ | ------ | ------ |
| ChatGPT      |  How to add robust fallback logic for date parsing in Python?      | It suggested using multiple fallback strategies.      |
| ChatGPT      |  How to compute age from two datetime objects considering incomplete birthdays accurately?      | It suggested 4 ways but I went with subtracting the birth year from the event year and adjusting if the birthday hasn't occurred.      |
| ChatGPT      | Is there a recommended structure for docstrings and inline comments?      | It suggested using triple-quoted docstrings for functions.
| ChatGPT      | Should I remove debugging comments?       | It suggested removing or commenting out debug prints after confirming functionality all together.       |
| ChatGPT      |  How to create a dictionary from a two-dimensional list for fast lookups?      | It suggested using a dictionary comprehension!       |
