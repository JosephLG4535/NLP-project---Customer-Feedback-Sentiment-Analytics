# NLP-project Customer Feedback Sentiment Analytics (Dashboard + ML Pipeline)

This repository contains files used in a self-made project. 
This project utilizes tools such as Python, Dash, Plotly, PostgreSQL and more to perform general end-to-end data science workflow process.
This project processes customer feedback data to analyze sentiment patterns using BERT-based NLP modeling. It includes a full interactive Plotly Dash dashboard for exploratory data analysis, word analysis, geographical insights, and time-based sentiment trends etc.

***DISCLAIMER*** 
This project is 100% done by the author with the help of online tools, discussions and forums. This project is not copied.
The dataset used in this project is obtained from https://www.kaggle.com/datasets/akxiit/blinkit-sales-dataset
**END OF DISCLAIMER***

Aim of the project :
1. For author to perform genereal end-to-end data science workflow process.
2. For author to understand the various tools and features self-learned by the author better.
3. For author to learn different functions and new discoveries on the tools used.
4. For author to learn new tools like Dash, CSS visualizations using Plotly and more.

Workflow of the project :
1. Simple dataset cleaning and pre-processing (Microsoft Excel / WPS)
2. EDA with some self thought use-cases (PostgreSQL / pgAdmin4)
3. Dashboard for EDA use-cases (Microsoft Excel / WPS / Excel Pivot)
4. Data processing for NLP & machine learning (Python)
5. Sentiment-feedback based analysis & visualizations (Python / Plotly)
6. Dashboard for Sentiment-feedback analysis visualizations (Python / Dash)

Improvements for the project :
1. The project uses NLPTown's BERT model as the base for machine learning model to learn from, hence, the computing time takes a while.
2. The author performed fine-tuning with hyperparameter and GridSearchCV on an already 100% accuracy model.
3. The author did not perform specific use-cases analysis with the predicted results from the model, only covered some general cases.
4. The author generate meaningful words in "word-based analysis" section with simple removal.
5. The cleaned dataset from SQL used for analysis section still required few processing for certain visualizations.
6. The dashboard formatting can still be improved. For instance, in "wordcloud analysis" dropdown the graph titles does not scale with zooms.
