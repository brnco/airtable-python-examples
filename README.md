# airtable-python-examples
a repo containing basic examples for how to implement the Airtable API in Python using [airtable-python-wrapper](https://airtable-python-wrapper.readthedocs.io/en/airtable-python-wrapper/)

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
"fields"{
  "Name":"Ursula Le Guin",
  "Date of Birth":"1929-10-21"
  }
}`

So, to access the date of birth info, you would use `record['fields']['Date of Birth']`

I find myself building dictionaries containing record information and then uploading that info
with either insert() or update():

with insert() you just send the dictionary

with update() you send the dictionary with a recordID, e.g.:

airtable_connection.update(recordID, {"field1":"value"})
