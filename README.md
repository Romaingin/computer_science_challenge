# Python Challenge web interface

Provide a simple interface for python training. The exercice is explained in details, and one can submit code which will be computed on the server side.

## Running the server

Use `sudo python server.py` to run the server through the port specified in the `server.py` file.

## Adding content

The description of the TD should go on the `exercices/description.des` file.
To create a new exercise, add a new `*.ex` file in the `exercices/` folder with the following structure :

```
Name of the exercice
###&###
Sample description
###&###
60 // Difficulty in percent
###&###
Explaination of the exercice here
###&###
Extra information
###&###
Information to give before submission (import, ...)
###&###
Actual imports in python
###&###
Python test code 2
#&#
Expected result 1
#&#
Python test code 2
#&#
Expected result 2
...
```

`###&###` are used as separators for parsing.
The exercices are added automaticaly.
