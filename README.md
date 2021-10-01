# airtable-python-examples
a repo containing basic examples for how to implement the Airtable API in Python using [airtable-python-wrapper](https://airtable-python-wrapper.readthedocs.io/en/airtable-python-wrapper/)

focused heavily on file operations/ cultural heritage work

contains examples for:
* uploading files to an attachment field
* downloading files from an attachment field
* using formulas to search a table
* calculating the number of unique records in a linked field

see the module documentation [here](https://airtable-python-wrapper.readthedocs.io/en/airtable-python-wrapper/api.html#)
for more basic examples, including:
* inserting records (i.e. add a new record to a table)
* updating records (i.e. adding new info to an existing record)

for authentication, see module documentation [here](https://airtable-python-wrapper.readthedocs.io/en/airtable-python-wrapper/authentication.html#module-airtable.auth)

additionally, Airtable provides really useful descriptions of every parameter
of every field in every table of YOUR base at [https://airtable.com/api](https://airtable.com/api)

## Things to keep in mind
In general, the following tips have helped me while working in this area

### Airtable records are dictionaries/ JSON objects

Example:

`{
"id":"rec1234abc",
"fields":{
  "Name":"Ursula Le Guin",
  "Date of Birth":"1929-10-21"
  }
}`

So, to access the date of birth info, you would use `record['fields']['Date of Birth']`

I find myself building dictionaries containing record information and then uploading that info
with either `insert()` or `update()`:

with `insert()` you just send the dictionary

with `update()` you send the dictionary with a recordID, e.g.

`airtable_connection.update(recordID, {"field1":"value"})`

### Airtable returns lots of things as lists

Your search results are lists, your get_all() is a list, your attachment fields are lists, etc.

These lists tend to be lists of dictionaries

### Linked records are linked on their record ID

Linked records are returned as their record ID/ list of record IDs,
to get the info in the linked record, use a second authenticated Airtable connection
to the table containing the linked record, as below:

`another_airtable_connection.get(recordID)`

If info in linked records is generally useful in the table they're being linked to,
consider adding them as a lookup field to avoid this step

### Mind your truthiness

In the API, a string value of "True" cannot be sent to a checkbox field as text, it has to be the Python boolean True,
although it displays in Airtable REST API docs as "true"

In the GUI, you can copy + paste data with Y/N or 1/0 and Airtable will make the conversion, but not so in the API

### Time

All durations are in seconds (hallelujah)

All dates are in ISO-8601 (also hallelujah)
