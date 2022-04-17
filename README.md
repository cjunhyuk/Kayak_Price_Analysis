# Kayak Plane Ticket Price Analysis
Author: Jun (Andrew) Choi
![Kayak Logo](/images/Kayak-Logo.png)

---
## <u>Table of Contents</u>

1. Business Understanding
2. Data
3. EDA and Data Cleaning
4. Modeling
5. Evaluation
6. Appendix

---

## <u>Business Understanding</u>
<p> In the era of covid where travel was few and far between many of us have been unable to travel.<br> 
However, looking optimistically into the future as covid <b>hopefully</b> becomes a thing of the past traveling will once again become a part of our lives.<br> 
With this in mind I sought to find when it would be the best time to purchase a ticket overseas or if there would be any specific features that could predict the prices of tickets over time.</p>

---
## <u>Data</u>

All of the data used in this analysis was gathered from [Kayak](https://www.kayak.com/flights) using a scraper from <b>Fabio Neves</b> [Github](https://github.com/fnneves/flight_scraper/blob/master/FlightScraper%20python%20bot%20for%20kayak.ipynb) [Medium](https://medium.com/@fneves/if-you-like-to-travel-let-python-help-you-scrape-the-best-fares-5a1f26213086)<br>
The code for the scraper was from 2019 so it did not work and required some modifications to properly scrape from Kayak.<br>
You can find the updated scrapers for both Windows and Mac OS in [py_files](https://github.com/cjunhyuk/plane_price_proj/tree/master/py_files).<br>

#### <u>Limitations</u>

<ul>
    <li>Data was gathered from only Kayak</li>
    <li>Data collection was conducted from 2022-Apr-3 to 2022-Apr-10</li>
    <li>Plane Tickets were restricted to only round trip tickets</li>
    <li>All departure and return dates were spaced 1 week apart</li>
    <li>Flights were gathered for a period of 4 months beginning at 2022-Apr-10 to 2022-Sep-1</li>
    <li>From the following locations</li>
    <ol>
        <li>New Jersey (EWR)</li>
        <li>New York (All Airports)</li>
        <li>California (SAN)</li>
    </ol>
    <li>To the following destinations</li>
    <ol>
        <li>Singapore</li>
        <li>South Korea</li>
        <li>Phuket, Thailand</li>
    </ol>
</ul>

---

## <u>EDA and Data Cleaning</u>

<p>After removing any possible duplicate entries I was left with 58,713 unique tickets.<br>
When assigning the targets to the data set the criterias I chose were:
<ol>
    <li>If the ticket price was in the bottom 25% of its respective dataset</li>
    <li>If the ticket overall duration was in the bottom 25% of its respective data set</li>
</ol>
Essentially what I wanted were the shortest and cheapest flights.<br>

![Targets](/images/Target%20Split.png)

Because of the class imbalance that was present it was essential to utilize [SMOTE](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html).<br>
To compile the master dataset I created a [compiler function](https://github.com/cjunhyuk/plane_price_proj/blob/master/py_files/cleaner.py) that combined all of the tickets from the specific routes.<br>
This was also where the target assigning and most of the feature enginering took place.
</p>

---

## <u>Modeling</u>

<p>The evaluation metric I decided to use was Accuracy and Precision.<br>
The reason I chose Precision is because I wanted more emphasis on identifying false postives so my model would not return a ticket that was not the cheapest and shortest duration.<br>
For the baseline model I chose to utilize a Dummy Classifier that produced an accuracy score of 50.63%. 
When running my first Logistic Regression Model it produced an accuracy score of 99.03% and precision score of 83.39%.<br>
Comparing this to the final model I decided to use which was a Decision Tree Classifier we can see a drastic improvement in model performance.<br>


![Line Plot](/images/Price%20Lineplot.png)