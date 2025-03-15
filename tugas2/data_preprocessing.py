import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset with a corrected file path
df = pd.read_csv('tugas2/Womens Clothing E-Commerce Reviews.csv')  # Forward slash

# After cleaning, show a before and after comparison of the data
print("Before cleaning:")
print(df.shape)
print(df.head())

# 1. Handle Missing Values
# Impute missing values in 'Title' with a placeholder, and drop rows with missing 'Review Text'
df['Title'] = df['Title'].fillna('No Title')  # Corrected to avoid chained assignment
df.dropna(subset=['Review Text'], inplace=True)

# 2. Remove Duplicates
df.drop_duplicates(inplace=True)

# 3. Normalize and Standardize Data
# Select numerical columns for normalization
numerical_cols = ['Age', 'Positive Feedback Count', 'Rating']
scaler = MinMaxScaler()  # You can use StandardScaler() for Z-score normalization instead
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# 4. Check Consistency
# Standardize categorical columns: remove extra spaces and lowercase
df['Division Name'] = df['Division Name'].str.strip().str.lower()
df['Department Name'] = df['Department Name'].str.strip().str.lower()
df['Class Name'] = df['Class Name'].str.strip().str.lower()

# 5. Outlier Detection using Boxplot (or statistical method)
# Example for 'Age' column
sns.boxplot(x=df['Age'])
plt.show()

# Remove outliers using the IQR method (Interquartile Range)
Q1 = df['Age'].quantile(0.25)
Q3 = df['Age'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['Age'] >= (Q1 - 1.5 * IQR)) & (df['Age'] <= (Q3 + 1.5 * IQR))]

# Save cleaned data to a new CSV
df.to_csv('cleaned_data.csv', index=False)

print("After cleaning:")
print(df.shape)
print(df.head())
