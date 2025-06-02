# Trending Video Analysis Summary

## Dataset Overview
This Tableau analysis examines the top 50 trending videos per country. The dataset includes fields like `Category`, `country`, `Views`, `Likes`, `Comments`, `Publish_Timestamp`, and `duration_minutes`, etc. The purpose is to identify patterns in video publishing, category trends, geographic distribution, and engagement.

## Key Insights from Visualizations

1. **Geographic Distribution**  
   - *Visualization*: Map using Latitude and Longitude.  
   - *Insight*: Total views of trending videos and the top category.

  ![Screenshot 2025-05-11 102948](https://github.com/user-attachments/assets/807aec99-f77a-4a7e-ad73-91cd954a42eb)


2. **Engagement Analysis**  
   - *Visualization*: Bar plot of Category vs Engagement.  
   - *Insight*: Entertaintment and Music videos exhibit high engagement (Likes per View).

  ![Screenshot 2025-05-11 103009](https://github.com/user-attachments/assets/3c45deb7-7ed0-472d-aeef-f860c470a338)


3. **Content Length Impact**  
   - *Visualization*: Bar chart of Views by binned `duration_minutes`.  
   - *Insight*: Shorter videos (0-5 minutes) drive more Views than longer ones.

![Screenshot 2025-05-11 103101](https://github.com/user-attachments/assets/63289e6a-0e8f-4b60-bcbd-66756de716bb)

   
4. **Growth Rate**  
   - *Visualization*: Bar chart of categories by average grwoth rate.  
   - *Insight*: Film & Animation, Entertaintment, Music, Sports lead showing category dominance.

![Screenshot 2025-05-11 103158](https://github.com/user-attachments/assets/53068a11-9600-4789-b655-864bcb0dc70c)


5. **Correlation**  
   - *Visualization*: Scatter plot of views by likes coloured by category.  
   - *Insight*: Higher views generally means people like the content.
  
![Screenshot 2025-05-11 103307](https://github.com/user-attachments/assets/f1720473-7026-4af3-817e-4c3a53ec0e05)


6. **Hourly Volume of Trending Videos**  
   - *Visualization*: Line plot of distinct video views by publish hour.  
   - *Insight*: Trending videos peak at 14:00 - 15:00 UTC (60+ videos), suggesting an optimal posting time.
  
![Screenshot 2025-05-11 103711](https://github.com/user-attachments/assets/135b4c47-7542-48b9-bd4d-31314d8b038a)

## Tableau Dashboard

<img width="802" alt="Dashboard 1" src="https://github.com/user-attachments/assets/c0c2d68e-7896-47d2-9abc-acb1802a8305" />


## Calculated Fields
- **`Publish_Date`**  
  Converts Unix timestamp to date.  
  `DATEADD('second', INT([Publish_Timestamp]), #1970-01-01#)`

- **`Publish_Hour`**  
  Extracts hour from `Publish_Date`.  
  `DATEPART('hour', [Publish_Date])`

- **`Engagement_Score`**  
  Measures engagement efficiency.  
  `([Likes] + [Comments]) / [Views]`

- **`Most_Frequent_Category`**  
  Finds the most frequent category per country.\
  `IF {FIXED [country], [Category] : COUNT([Video_Id])} = {FIXED [country] : MAX({FIXED [country], [Category] : COUNT([Video_Id])})}
THEN [Category]
ELSE NULL
END` 


## Overall Learnings
Creators can leverage these findings by targeting evening releases, focusing on popular categories, and keeping videos concise for maximum impact.
