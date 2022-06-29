# Recruitment task

## General information
The seller has an e-commerce store with various products. So far, trade has been carried out on
in Poland. The seller would like to ship goods to European Union countries and to the United States
United. Therefore, he needed to accept payments in US dollars
(USD) and in Euro. The buyer needs to know how much the goods cost in a given currency.
The seller needs a solution that will periodically download the current one once a day or on request
exchange rate from the National Bank of Poland and will update prices for products in the database.

## Features
- Connects to NBP API, gets current USD and EUR currency ratio and executes update query to database.
- By default, updates database on app start and every 12 hours. This update can also be executed on demand
- On demand queries all products from database and saves it to Excel file.


### Note
Data provided to import into database was throwing errors. This happend because table was set to CHECK (USER_TYPE = 'S'),
where provided data has records with only USER_TYPE = 'B', so I needed to alter database a little to accept anything at all.

### Author
patrykciesz@gmail.com
