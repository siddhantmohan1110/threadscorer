# Trending Post Scoring

> **Note:** All counts are by unique users to eliminate bot activity.

## Variables

| Symbol | Description                                 | Default Value / Weight |
|--------|---------------------------------------------|-----------------------|
| **S**  | Number of shares or reposts                 |                       |
| **O**  | Number of other interactions <br>*(e.g., bookmarks, follows — define as needed)* |                       |
| **C**  | Number of comments or replies               |                       |
| **L**  | Number of unique likes                      |                       |
| **D**  | Number of unique dislikes                   |                       |
| **Vc** | Number of unique cursory views <br>*(< 2s)* |                       |
| **Ve** | Number of unique engaged views <br>*(≥ 2s)* |                       |
| **a₁** | Weight for likes                            | 0.8                   |
| **a₂** | Weight for dislikes                         | 0.1                   |
| **b₁** | Weight for cursory views                    | 0.1                   |
| **b₂** | Weight for engaged views                    | 0.3                   |

## Weights

| Weight | Applies To                | Default Value |
|--------|--------------------------|--------------|
| **w₁** | Shares/Reposts (**S**)   | 0.35         |
| **w₂** | Other Interactions (**O**)| 0.25         |
| **w₃** | Comments/Replies (**C**) | 0.25         |
| **w₄** | Likes/Dislikes (**L, D**) | 0.10         |
| **w₅** | Views (**Vc, Ve**)       | 0.05         |

*All weights and variable values can be adjusted via the Admin Panel.*

---

## Normalized Trending Post Score

$$
\text{Total Interactions (T)} = S + O + C + (a_1 \cdot L + a_2 \cdot D) + (b_1 \cdot V_c + b_2 \cdot V_e)
$$

$$
\text{Normalized Trending Post Score} = \left[ w_1 S + w_2 O + w_3 C + w_4 (a_1 L + a_2 D) + w_5 (b_1 V_c + b_2 V_e) \right] \cdot \left( \frac{100}{T} \right)
$$

---

## Time-Weighted Trending Post Score

- **Base Timeframe:** 7 days (split into 7 daily periods: P₁, P₂, ..., P₇)
- **Step 1:** Calculate daily scores S₁, S₂, ..., S₇ for each period.
- **Step 2:** Compute total score \( S_t = S_1 + S_2 + ... + S_7 \).
- **Step 3:** Apply time decay weights:

$$
X_k = e^{-n_k \cdot D_c}
$$

- **n<sub>k</sub>**: Number of periods since the current one (e.g., 0 for today, 1 for yesterday, etc.)
- **D<sub>c</sub>**: Decay constant (default: 0.1, adjustable 0.001–0.99)

$$
\text{Time-Weighted Score (Pf)} = \frac{(X_1 S_1 + X_2 S_2 + ... + X_7 S_7) \cdot 100}{S_t}
$$

---

## Trending Category/Topic/Asset Score

**Trending Category Score:**  
$$
= \frac{\text{Sum of Pf for each post in the Category}}{\text{Number of posts in that Category}}
$$

**Trending Topic Score:**  
$$
= \frac{\text{Sum of Pf for each post in the Topic}}{\text{Number of posts in that Topic}}
$$

**Trending Asset Score:**  
$$
= \frac{\text{Sum of Pf for each post in the Asset}}{\text{Number of posts in that Asset}}
$$

---

*For any questions or to adjust parameters, use the Admin Panel.*
