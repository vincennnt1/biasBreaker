# biasBreaker

biasBreaker is a fake news detector for online articles. There is an application where you can paste a link, and an extension that allows you to check whenever you are on an article's webpage.

## Features
- Uses a custom NLP model to assign a value to how likely it is that an article is true, based on the title and the text.
- Keeps a history of your past searches on the app.
- Application starts a local server so that the extension can send the webpage data to the model, and bring the results directly to your browser.

## Usage

1.  Launch Application. This also launches the local server/API.
2.  Paste a link into the textbox and find out the article's rating.
3.  You can also open Chrome and use the extension to find out an article's rating.

## Tech Stack

- **Python**  
- **Natural Language Processing** (custom NLP model)  
- **Data analysis libraries** (e.g., pandas, numpy, scikit-learn)
- **CustomTkinter** (GUI for Windows)
- **Javascript** for Chrome Extension
- **Flask** to set up local API

## Data Set Source

Obtained from [Kaggle](https://www.kaggle.com/datasets/emineyetm/fake-news-detection-datasets/data)


Click the link above to download the app.
