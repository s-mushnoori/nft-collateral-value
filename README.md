# nft-collateral-value
Calculating the collateral value of NFT projects. The initial problem statement and data was part of an [interview question](https://metastreet.notion.site/Senior-Data-Scientist-Engineer-bad2e7e9a8e340d3a23ff77faa56548d) for Metastreet Labs. The same concept was applied to data for other NFT projects obtained from the [CharlieDAO](https://github.com/charliedao-eth/NterpriseFT/tree/main/data) GitHub Repo. 

The final result can be viewed on the live webapp [here](https://nftcvcalculator.herokuapp.com/). Note that the app may take a moment to load if it has been idle for a while. 

---

# Table of Contents
1. &nbsp; **Business Problem**

2. &nbsp; **Data**

3. &nbsp; **Data Processing**
  
    3.1. &nbsp;&nbsp;&nbsp; Standardizing datasets
    
    3.2. &nbsp;&nbsp;&nbsp; Data cleaning
    
    3.3. &nbsp;&nbsp;&nbsp; Creating processed dataframes
    
    3.4. &nbsp;&nbsp;&nbsp; Calculating collateral floor price
    
    3.5. &nbsp;&nbsp;&nbsp; Visualization

4. &nbsp; **Deployment**

5. &nbsp; **Future Considerations**

---
## 1. &nbsp; Business Problem

An NFT is essentially a means to prove ownsership of a digital asset. A digital asset, like any other asset, can be used as collateral to borrow money against. But how do we determine the collateral value of a volatile asset? The purpose of this project is to create an automatic collateral value calculator from NFT transaction data. 

Here's a formula that calculates the collateral's floor price:

<img  src="https://github.com/s-mushnoori/nft-collateral-value/blob/main/Images/cv_formula.jpg" width=600>

---
## 2. &nbsp; Data

The data for this project comes from two different sources. 

The first source is the Metastreet Labs page. This dataset contains data for the Cryptopunks NFT project. This dataset has the following columns:

`buyer_address`,	`eth_price`,	`usd_price`,	`seller_address`,	`day`,	`utc_timestamp`,	`token_id`,	`transaction_hash`,	`name`,	`wrapped_punk`. 

The second source is the CharlieDAO GitHub repository. Three datasets were used from this source, the BAYC, MAYC and World of Women NFT projects. These datasets contain the following columns:

`BLOCK_TIMESTAMP`,	`EVENT_FROM`,	`EVENT_TO`,	`PRICE`,	`PROJECT_NAME`,	`TOKEN_ID`,	`TX_CURRENCY`,	`TX_ID`

To calculate collateral value, we only need the date of transaction and the price. An identifier with the name of the project, and the unique transaction IDs will also prove to be useful when it comes to data processing which will be discussed in the next section. 

It is also worthwhile to note that the Cryptopunks dataset also lists the price of the transaction in USD. This is much more intuitive for most people, who do not think of Ethereum as its own currency. Unfortunately, the second data source did not contain this information. There are ways to work around this, and one method will be discussed in the 'Future Considerations' section. For the sake of simplicity however, this project will only list collateral floor prices in Eth. 

---
## 3. &nbsp; Data Processing

The notebook describing the data processing can be viewed [here](https://github.com/s-mushnoori/nft-collateral-value/blob/main/Notebooks/EDA.ipynb).

### 3.1 &nbsp; Standardizing datasets

We can see in the section above that the datasets have different columns. To make the data easier to process, we will first change the column names of the Cryptopunks dataset to match the others, as shown below:

`day` --> `BLOCK_TIMESTAMP`

`eth_price` --> `PRICE`

`transaction_hash` --> `TX_ID`

Further, we will add a column titled `PROJECT_NAME` to this dataset and populate with the string value 'Cryptopunks'. 


### 3.2 &nbsp; Data cleaning

Now that we have the required columns in the desired format, we can clean the data. This is done through a function `clean_data` that uses the following steps:

1. First, we filter the datasets and select only the 4 columns of interest (described above). 

2. We convert the `BLOCK_TIMESTAMP` column to type datetime for easy manipulation.

3. Since there are very few null values, and there is no way to meaningfully impute these missing values, we drop rows with missing values.


### 3.3 &nbsp; Creating processed dataframes

With this out of the way, we can now create columns that will make this calculation easier. This is done by writing a function `create_cv_dataset` which carries out the following steps for each dataset:

1.  Filter out 0.15 x (Q1 of daily transactions) as per the collateral value definition

2.  Calculate the number of daily transactions

3.  Calculate the daily price floor

4.  Create and return a new dataset with the date, daily price floor, and number of daily transactions


### 3.4 &nbsp; Calculating collateral floor price

Finally, we calculate the collateral floor price through the function `calculate_cv` based on the formula for the collateral floor price. 

As an additional step, we can combine these datasets for ease of use when deploying to a web app. 


### 3.5 &nbsp; Visualisation

The colalteral floor price can also be visualized. This is what it looks like for the Cryptopunks dataset:

<img  src="https://github.com/s-mushnoori/nft-collateral-value/blob/main/Images/cryptopunks_cv.jpg" width=450>

---

## 4. &nbsp; Deployment

A simple dashboard was created using Plotly Dash and deployed to the web using Heroku.

The code for the plotly dashboard can be found in the file `app.py`. The Heroku webapp can be accessed by using this [link](https://nftcvcalculator.herokuapp.com/).

---

## 5. &nbsp; Future Considerations

1. &nbsp; This project only used the Eth price to calculate the collateral floor price because 3 out of the 4 datasets did not contain USD transaction data. 
 
    - &nbsp;&nbsp; This can be worked around by averaging the daily Eth Price from the first dataset and imputing it to the other 3. Though not perfect, this could give a very close approximation to having the actual transaction data in USD.

2. &nbsp; It is always a good idea to refactor and generalize the code from the notebooks to a .py file. 

    - &nbsp;&nbsp; The next step would be to generalize the code, so adding a new dataset would only require adding one line of code to a list of relevant datasets.

3. &nbsp; An interesting feature to add to the dashboard would be to compare the collateral floor prices for different projects. 

    - &nbsp;&nbsp; This could enable us to discover how different projects perform relative to each other during changing market conditions, and would be very useful information to consider before investing in a project. 

4. &nbsp; Another useful quality-of-life feature to add to the dashboard would be to freeze dates outside of the date ranges for each project.

    - &nbsp;&nbsp; The four datasets each have data available for different date ranges. Currently the dashboard works under the assumption that the user inputs a date in the correct range for each project. It would be useful to dynamically modify the available dates based on the user chosen project. 
