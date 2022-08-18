# zelands
2d multiplayer RPG with guns and questionable coding practices

# Creating and Updating python depenencies

The below commands will create a requirements.txt that can be used to install all dependencies at once.

    pip install pipreqs
    pipreqs . --force

Run the below command to install all the required dependencies


    ```pip install -r requirements.txt```




# Twisted server

To start the twisted server, do:

```
set PYTHONPATH=%CD%
twistd zelands_server
```