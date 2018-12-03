# Blizzard forum sentiment-to-stock price graphed

Will scrape sections of blizzard forums every 15 minutes and create a file with date, thread title, post sentiment, and section posted in. 

Grapher.py will use this data to create a visualization showing daily sentiment values and stock price values.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required dependencies.

```bash
pip install matplotlib
pip install pandas
pip install pandas-datareader
pip install textblob
pip install beautifulsoup4

```

You will also need to download the TextBlob standard corpora using
```bash
python -m textblob.download_corpora
```

## Usage

Run getPosts.py - this will create a file named 75subjectivity.csv and upload posts with over 75 subjectivity to it.

Once enough data is collected run Grapher.py for a visualization of collected data.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
