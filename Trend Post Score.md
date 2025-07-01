

## Trending Post

**Normalized Trending Post Score** $$= \frac{(w_1 \cdot \text{reposting/sharing} + w_2 \cdot \text{Commenting/reply} + w_3 \cdot \text{likes plus dislikes} + w_4 \cdot [a_1 \cdot \text{cursory view} + a_2 \cdot \text{engaged view}])}{\text{Total Interactions}}$$

**Total Interactions** $$= (\text{reposting/sharing} + \text{Commenting/reply} + \text{likes plus dislikes} + [a_1 \cdot \text{cursory view} + a_2 \cdot \text{engaged view}])$$
*Note: This denominator normalizes it so that the resulting score is not too large.*

## Modified Normalized Trending Post Score

* **S**: Number of Shares or reposting
* **O**: Number of Other Interactions
* **C**: Number of Comments or replies
* **L**: Number of Unique Likes
    * **a1**: 0.8 (Weighting Likes 8X more than dislikes)
* **D**: Number of Unique Dislikes
    * **a2**: 0.1 (Weighting Dislikes much lesser than Likes)
* **Vc**: Number of Unique cursory views
    * Cursory View: Less than 2 seconds
    * **b1**: 0.1
* **Ve**: Number of Unique engaged views
    * Engaged View: More than 2 seconds
    * **b2**: 0.3

**Total Interactions (T)** $$= [S + O + C + (a_1 \cdot L + a_2 \cdot D) + (b_1 \cdot V_c + b_2 \cdot V_e)]$$

**Normalized Trending Post Score** $$= [w_1 \cdot S + w_2 \cdot O + w_3 \cdot C + w_4 \cdot (a_1 \cdot L + a_2 \cdot D) + w_5 \cdot (b_1 \cdot V_c + b_2 \cdot V_e)] \cdot (100/T)$$

**Weights**
*We should be able to change these weights through the Admin Panel overtime*
* w1: 0.35
* w2: 0.25
* w3: 0.25
* w4: 0.10
* w5: 0.05

*Each of these are "numbers" of posts, comments, views, likes, dislikes etc. BY UNIQUE USERS (This will eliminate the BOT issue).*

## Time Weighted Trending Post Score with Decay Function

* **BaseLine Timeframe**: 24 hours or 1 week?
    * *If it is 1 week then it could just be the same user as it would take 1 week's time to change it. But if it 24 hours then the trending will change everyday BUT there may not be enough data.*
    * *SOLUTION TO THIS IS USING A DECAY FUNCTION THAT WEIGHTS IT BY TIME*

* **Total Time Period**: 7 Days
* **Sub Periods**: 24 hour individual periods (7 periods: P1, P2, ... P7)

* **Step 1**: Calculate Score, S1, S2…S7, for each period P1, P2…P7.
* **Step 2**: Calculate St = S1 + S2 + S3 +S4 + S5 + S6 + S7.
* **Steps 3**: Calculate Pf

**Time Weighted Normalized Trending Post Score (Pf)** $$= \frac{(X_1 \cdot S_1 + X_2 \cdot S_2 + X_3 \cdot S_3 + X_4 \cdot S_4 + X_5 \cdot S_5 + X_6 \cdot S_6 + X_7 \cdot S_7) \cdot 100}{S_t}$$

Where X1, X2….X7 are defined below:

**Time Weights**
* **$$X_{k}$$** $$= e^{(-n_k \cdot D_c)}$$
    * Where _k_ = 1, 2, 3, 4, 5, 6, 7


* **Dc**: Decay Constant
    * Value can range from .001 to 0.99
    * We will start with 0.1

*We should be able to change all the values of VARIABLES from the Admin Panel.*

## Formulae: Trending Category/Asset/Topic

*Same formula would be used for Trending Topic & Trending Assets.*

*For trending category, use a similar formula as for the Trending Post, but aggregate the scores for each post in a particular category. So,*

**Trending Category Score** $$= \frac{\text{Sum of (Pfs for each post in the Category)}}{\text{Number of posts in that Category}}$$

**Trending Topic Score** $$= \frac{\text{Sum of (Pfs for each post in the Topic)}}{\text{Number of posts in that Topic}}$$

**Trending Asset Score** $$= \frac{\text{Sum of (Pfs for each post in the Asset)}}{\text{Number of posts in that Asset}}$$

---
