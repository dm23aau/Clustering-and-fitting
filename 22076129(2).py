import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.metrics as skmet
from sklearn.preprocessing import MinMaxScaler
import sklearn.cluster as cluster

# This function determines the relationship between x and y values of the curve y=f(x).
def polynomial_curve(x, *coefficients):
    return sum(c * x**i for i, c in enumerate(coefficients))

# Plotting k clusters using k-means clustering.
def plot_kmeans(data, num_clusters):
    scaled_data = min_max_scaler(data.iloc[:, 1:])
    kmeans = cluster.KMeans(n_clusters=num_clusters)
    kmeans.fit(scaled_data)
    cluster_centers = kmeans.cluster_centers_

    # Print the coordinates of the cluster centers.
    for i in range(num_clusters):
        print(f'The coordinates of the center of cluster {i + 1} are ({cluster_centers[i, 0]}, {cluster_centers[i, 1]})')

    # Print the silhouette score.
    silhouette_score = skmet.silhouette_score(scaled_data, kmeans.labels_)
    print(f'The Silhouette score of the clusters is {silhouette_score}')

    # Plotting the scaled clusters.
    plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=kmeans.labels_)
    plt.xlabel('CO2 Emission (Scaled values)')
    plt.ylabel('Access to Electricity (Scaled values)')
    plt.title('K-means clustering')
    
    for center in cluster_centers:
        plt.plot(center[0], center[1], "*", markersize=10, c='r')
    
    plt.show()
    return kmeans

# Finding a sample from ith cluster.
def find_sample_from_cluster(labels, cluster_number):
    return next(i for i, label in enumerate(labels) if label == cluster_number)

# Curve fitting of electricity data using a polynomial fit.
def fit_curve(X, Y, degree):
    # Convert Y to numeric type if needed
    Y = pd.to_numeric(Y, errors='coerce')

    if Y.isnull().any():
        raise ValueError("Invalid data in the column. Ensure all values are numeric.")

    coefficients = np.polyfit(X, Y, degree)
    polynomial_fit = np.poly1d(coefficients)
    
    # Plotting the original data and the polynomial fit.
    plt.scatter(X, Y, label='Original Data')
    x_line = np.linspace(min(X), max(X), 100)
    y_line = polynomial_fit(x_line)
    plt.plot(x_line, y_line, '--', color='b', label=f'Polynomial Fit (Degree {degree})')
    plt.xlabel('Year')
    plt.ylabel('CO2 emission in kt')
    plt.title('Polynomial Curve Fitting of CO2 emission in Brazil')
    plt.legend()
    plt.show()

    # Predicting the future values from the polynomial fit.
    future_years = [2020, 2021, 2022, 2023, 2024]
    for year in future_years:
        predicted_value = polynomial_fit(year)
        print(f'The predicted CO2 emission in kt in Brazil in {year} is {predicted_value}')

# This function plots the elbow plot of different  number of clusters.
def elbow_plot(data):
    data = min_max_scaler(data.iloc[:, 1:])
    inertias = []
    for i in range(10):
        kmeans = cluster.KMeans(n_clusters=i + 1)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)
    
    plt.plot(range(1, 11), inertias, marker='*')
    plt.title('Elbow Graph to determine the optimal number of clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()

# Min Max Scaler function changes the range of the data to [0, 1]
def min_max_scaler(data):
    scaler = MinMaxScaler()
    scaler.fit(data)
    return scaler.transform(data)

# Loading the data
co2_df = pd.read_csv('co2_emission_data.csv')
electricity_df = pd.read_csv('access_to_electricity_data.csv')

data = pd.DataFrame({
    'Country Name': co2_df.iloc[:, 0].values,
    'CO2 Emission': co2_df.iloc[:, 60],
    'Access to electricity': electricity_df.iloc[:, 60]
})

# Dropping rows with missing values
data = data.dropna()

# Drawing the elbow graph to find the optimal number of clusters in K-means algorithm and then plotting the k means clusters.
elbow_plot(data)
kmeans = plot_kmeans(data, 3)

# Comparing the two countries of different clusters.
first_country = find_sample_from_cluster(kmeans.labels_, 0)
second_country = find_sample_from_cluster(kmeans.labels_, 1)
third_country = find_sample_from_cluster(kmeans.labels_, 2)
print(data.iloc[[first_country, second_country, third_country], :])

# Curve fitting
fit_curve(range(1991, 2020), co2_df.iloc[29, 35:64], degree=4)  
