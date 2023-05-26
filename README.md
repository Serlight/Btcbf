
# Btcbf  [![CodeFactor](https://www.codefactor.io/repository/github/vlnahp/btcbf/badge/main)](https://www.codefactor.io/repository/github/vlnahp/btcbf/overview/main)
Btcbf is a fast and efficient bitcoin private key brute force tool written in python. It works based on generating random or sequential private keys and their corresponding public address. Then checking the address through an online API or an offline database.

What makes Btcbf fast, is mainly the bit library. Thanks to its developer!

## **Quick Start**
```
 $ git clone https://github.com/vlnahp/Btcbf.git

 $ cd Btcbf

 $ pip install -r requirements.txt

 $ python Btcbf.py or  $ python3 Btcbf.py on Linux
```


92322265-1-100000000000

april parent life merge river frog auto foot captain midnight under mango


 {
  "phrase": "slogan brush favorite pole climb other ill sudden mask bounce miracle hello",
  "primary": {
    "address": "bc1prg72dvpknzqx0zka04y78vnzedjmtjuv257fc7t0030lps00wneqr5hx5f",
    "path": "m/44'/0'/0'/0/0",
    "WIF": "L4g8E4PajMRc4vGkHfd7VQ2TJGyANbr9E53z2yyKiRkTP9ZFzPDq"
  },
  "funding": {
    "address": "bc1p80hlrgq5s53w3y8nnhu6x787c9a3kcgm4eum46vrdp7mm9hpxfhqu033zd",
    "path": "m/44'/0'/0'/1/0",
    "WIF": "L2h8ZpeyXXVihvsCQ5LCJhnkSGJmPc365e2opj3J93mkezdkXGEM"
  }
}

{
  "phrase": "april parent life merge river frog auto foot captain midnight under mango",
  "primary": {
    "address": "bc1ptsmsc0nwelk4lmluefxspv7xwkvglap9tedudr2ze83ml3mt2hwsz0kz6c",
    "path": "m/44'/0'/0'/0/0",
    "WIF": "L4uKjbX6tYMqVoBpHQ77jvq4FQvrkfW15U3ZKkh3Yf5qcYXkZtK4"
  },
  "funding": {
    "address": "bc1pzvrl5a2d3wvyj9zz4schpwjp3up2kutzzaazr5j7lujt2fglywhsjc57mw",
    "path": "m/44'/0'/0'/1/0",
    "WIF": "L4XMLx6U72bUdDWGtvboNUBkxNxY5kzxEsxwqFTmb2X8ybj6SQyJ"
  }
}

{
  "phrase": "elegant such check turkey genuine popular pact grant sister lend seed divert",
  "primary": {
    "address": "bc1pts63ty62au3fhs7qsgxejjzn7u7v84v5vgcqs5t2vqxhaj6434zqjnfnlr",
    "path": "m/44'/0'/0'/0/0",
    "WIF": "L3m13gS87DNZ1b3mtEaDJQDc4HtRjsfj8hGnULeKhsEBep4bczii"
  },
  "funding": {
    "address": "bc1p7fzyhy3rejhk0emy0a448fmpkewrctu2lv0dqpzl6z02uc85cm9qsv4puh",
    "path": "m/44'/0'/0'/1/0",
    "WIF": "L4sNxySDVhNAK7BSHXztNRKTEX3F1tzrVdaLYSDqZS3YFq8umoPJ"
  }
}






## The Goal
The main goal is to ~~prove bitcoin is secure. At least until the day that Quantum computers start working against it~~ learn python! 

There are also some useful tools implemented.



## **Requirements**

  In offline mode, a database is necessary. By default, it is `address.txt` containing some addresses. Let's be honest, searching online takes too long and the addresses with balance included in the program are too scarce (as having a current text file with all addresses would make this repository over 5GB). So the users who wish, can download the latest text file from [here](http://addresses.loyce.club/) (direct [link](http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz)), rename and replace it with the "address.txt". But be careful about memory issues. Only use this database if you have sufficient RAM!

To install the requirements run the command below:

```$ pip install -r requirements.txt```  


## **Usage**
Just execute this command: `$ python Btcbf.py` or `$ python3 Btcbf.py` on Linux, Btcbf tells you what to do!

Type your desired action and follow instructions. (I love to interact with my program🙂)

Results will be saved to `foundkey.txt` in the main directory.

## **Licence**

Permissions of this strongest copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights. When a modified version is used to provide a service over a network, the complete source code of the modified version must be made available.




## Latest Release
Link to latest release(v1.2.0): [link](https://github.com/vlnahp/Btcbf/releases/download/v1.2.1/Btcbf-windows64-v.1.2.0.tar.xz)
