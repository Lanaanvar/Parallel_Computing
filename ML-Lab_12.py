import numpy as np
from sklearn.metrics import pairwise_distances_argmin
from scipy.spatial.distance import cdist

def k_means(data, k, max_iter=100):
    np.random.seed(42)
    centroids = data[np.random.choice(range(len(data)), k, replace=False)]
    
    for _ in range(max_iter):
        labels = pairwise_distances_argmin(data, centroids)
        new_centroids = np.array([data[labels == i].mean(axis=0) for i in range(k)])
        
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    
    return labels, centroids

def k_medoids(data, k, max_iter=100):
    np.random.seed(42)
    medoids = data[np.random.choice(range(len(data)), k, replace=False)]
    
    for _ in range(max_iter):
        distances = cdist(data, medoids, metric='euclidean')
        labels = np.argmin(distances, axis=1)
        new_medoids = np.array([data[labels == i][np.argmin(cdist([medoids[i]], data[labels == i], metric='euclidean').sum(axis=1))] for i in range(k)])
        
        if np.all(medoids == new_medoids):
            break
        medoids = new_medoids
    
    return labels, medoids

def fuzzy_c_means(data, k, m=2, max_iter=100, epsilon=1e-5):
    np.random.seed(42)
    n_samples, n_features = data.shape
    u = np.random.rand(n_samples, k)
    u = u / np.sum(u, axis=1, keepdims=True)

    for _ in range(max_iter):
        centroids = np.dot(u.T ** m, data) / np.sum(u.T ** m, axis=1, keepdims=True)
        distances = cdist(data, centroids, metric='euclidean')
        new_u = 1 / (distances ** (2 / (m - 1)) + 1e-10)
        new_u = new_u / np.sum(new_u, axis=1, keepdims=True)

        if np.linalg.norm(new_u - u) < epsilon:
            break
        u = new_u

    return u, centroids

# Example usage:
if __name__ == "__main__":
    from sklearn.datasets import make_blobs

    # Generate synthetic dataset
    data, _ = make_blobs(n_samples=300, centers=3, cluster_std=1.0, random_state=42)

    # K-means
    kmeans_labels, kmeans_centroids = k_means(data, k=3)
    print("K-means Centroids:\n", kmeans_centroids)

    # K-medoids
    kmedoids_labels, kmedoids_medoids = k_medoids(data, k=3)
    print("K-medoids Medoids:\n", kmedoids_medoids)

    # Fuzzy C-means
    fuzzy_membership, fuzzy_centroids = fuzzy_c_means(data, k=3)
    print("Fuzzy C-means Centroids:\n", fuzzy_centroids)
