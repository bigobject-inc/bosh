# BOSH - a BigObject shell

**bosh** is a python command-line interface for a BigObject server

##System requirements
Python 2.7

Packages: bosh-dumpRes, bosh-db2bt

## Getting BigObject

BigObject server provides storage and analytic computation for your data.
These feature endpoints are made available through BigObject query language,

Refer to the full documentation [here](https://docs.bigobject.io/)

We recommend you build your BigObject server through
[Docker Hub](https://registry.hub.docker.com/u/macrodata/bigobject/).  Other options available through custom
request via info@macrodatalab.com

## Getting BOSH

The recommended way for getting BOSH is through the python package management tool "pip" :

```bash
$ pip install bosh
```

**pip** is a popular python package management tool.  Get pip
[here](https://pip.pypa.io/en/latest/installing.html)

Verify bosh is install be excuting **bosh** in your terminal
 
Use the environment variable **BIGOBJECT_URL**  to set the BigObject server url

ex. BIGOBJECT_URL=bo://127.0.0.1:9090 bosh

The default BIGOBJECT_URL setting: localhost:9090 

```bash
$ BIGOBJECT_URL=<url_to_bigobject_service> bosh
Welcome to the BigObject shell

enter 'help' for listing commands
enter 'quit'/'exit' to exit bosh
bosh>
```

# bosh features
## change server
```bash
bosh>sethost 192.168.1.111
bosh>setport 9090
```

## csvloader
Load a table data from a CSV file (ex. data.csv). The table (ex. datatable) should be pre-created.
```bash
bosh>admin
bosh:admin>csvloader data.csv datatable
bosh:admin>exit
bosh>
```
If you ensure the CSV file without any control character, use 'boost' mode to speed up data insertion.
```bash
bosh:admin>csvloader data.csv datatable boost
```
Assign number of csv rows in an insert statement
```bash
bosh:admin>csvloader data.csv datatable 50
bosh:admin>csvloader data.csv datatable boost 50
```

## luaupload
Upload a lua script to the BigObject server
```bash
bosh>admin
bosh:admin>luaupload test.lua
bosh:admin>exit
bosh>
```

## copy/append/load tables from mysql/~~postgresql~~ database
Temporal remove postgresql part because of the dependence issue
```bash
bosh>setdb
>>> database type [postgresql] : mysql
>>> host [localhost] : 
>>> port [5432] : 3306
>>> username [postgres] : root 
>>> Password (hidden) : 
>>> database name [test] : 
bosh>copy sales
     ...
bosh>append sales
     ...
bosh>load sales by select * from sales limit 100
     ...
bosh>showdb
db type:	mysql
db name:	test
host:		localhost:3306
user:		root
```

## dump data to csv
Automatically dump to csv file (default: return data > 1000 rows)
```bash
bosh>select * from sales
1,3226,2557,am/pm,2013-01-01 00:04:04,8,52.24
2,6691,2631,am/pm,2013-01-01 00:11:26,4,39.72
2,6691,1833,am/pm,2013-01-01 00:21:02,1,6.9

                ...
568,7717,4373,7-11,2013-01-05 00:16:12,3,33.72
569,7928,3351,walmart,2013-01-05 00:25:16,2,20.92
570,5218,2032,am/pm,2013-01-05 00:29:16,4,50.72
Size of data exceeded display limit, dump to csv format? (yes/no)
```
Manually dump
```bash
bosh>select * from sales >>> dump1.csv

bosh>select * from sales >>> dump2.xlsx
```
The Function only work on statement with a return table such as **FIND**, **SELECT**, **GET**, and **\*APPLY**

\*APPLY with the returnTable auxiliary clause

## Autocomplete

bosh automatacally load table and tree names into the autocomplete keywords when bosh init, perform "show tables" and "show tree".

## send / receive command

### send
send the result of a query to a shell command

    SEND "bigobject statement" TO "shell command"
    
ex. send query to the cut command to get the fifth field.

```
bosh>send "select * from sales limit 2" to "cut -d',' -f5"
2013-01-01 00:04:04
2013-01-01 00:11:26
```

### receive
receive a table from shell command. 

Note: the table need to be created before receiving data

The default delimiter is ' ' so return data with space would not be inserted correctly.

    RECEIVE table_name FROM "shell command"

ex. receive data from a json text file "json.txt"
```
{
   "data": [
      {"id": "X999_Y999"},
      {"id": "X998_Y998"} 
   ]
}
```
```
bosh>CREATE TABLE tmp (col1 STRING)
bosh>RECEIVE tmp FROM "cat json.txt | jq .data[].id --raw-output"
X999_Y999
X998_Y998
```

### send then receive

    SEND "bigobject statement" TO "shell command" RETURN TO table_name

```
bosh>create table tmp2(time STRING)
bosh>send "select * from sales limit 2" to "cut -d',' -f3" return to tmp2
2557
2631
bosh>select * from tmp2
2557
2631
=============
total row : 2
```

NOTE: the basic purpose is to link the BigObject data and a python program to perform high-level application (ex. k mean, machine learning and so on)

Please refer [bosh-pyfunc](https://github.com/bigobject-inc/bosh-pyfunc) for detail.

