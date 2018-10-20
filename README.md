
# Restonic

'Restonic' is an Open Source CLI tool intended to solve the Cluster-Management problem for the IBM Datapower Product.

The main purpose for 'Restonic' is to be reliable for managing a cluster of datapowers, with an intention to be fast and customizeable as well.

'Restonic' lets you create, modify and delete configuration  objects on any amount of Datapowers at once without transfering from one managment tool to another.
'Restonic' also lets you copy and move configurations from one Datapower to a numerous number of Datapowers with one single command

# Todo

## config.py

- Refactor the configuration file to be able to have multiple datapowers from multiple environments
- Create a function that returns an organized list of datapowers from the configuration file for an easy use in commands

## commands 

- Add an option to specify which datapower apply the command to. 
For example: when the option '--machine' is used, check if the given value exists within the configuration as a datapower.
In case the given value is 'all', apply the command to all of the datapowers from the configuration file.
If the given value isnt a datapower or the word 'all', return an error message.

## mpgw_commands.py

- Create a function that returns a list of MultiProtocol Gateways Names from a specific datapower / environment / all of them.
- Create a function that modifies a given MultiProtocol Gateway.
