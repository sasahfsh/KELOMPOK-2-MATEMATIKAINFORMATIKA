import math
import random

gedung = {
    "FPMIPA A": [4.4, 3.9, 4.3],
    "FPMIPA B": [4.4, 3.8, 3.9],
    "FPMIPA C": [4.1, 3.6, 3.5],
    "FPTI A": [4.0, 4.0, 4.5],
    "FPTI B": [3.3, 3.6, 3.6],
    "FPTI C": [3.3, 3.8, 3.5],
    "FPTI D": [5.0, 5.0, 5.0],
    "FIP Lama": [3.8, 2.8, 3.0],
    "FIP Baru": [4.0, 4.0, 3.8],
    "FPBS A": [4.2, 3.4, 3.6],
    "FPBS B": [4.0, 3.6, 3.6],
    "FPOK A": [3.7, 3.6, 3.5],
    "Kolam Renang": [3.0, 3.6, 3.2],
    "Gymnasium": [3.2, 3.4, 3.2],
    "Sports Hall": [3.4, 3.4, 3.6]
}

K = 3
max_iter = 100

# ubah ke list
nama_gedung = list(gedung.keys())
data = list(gedung.values())

centroids = random.sample(data, K)

def euclidean_distance(a, b):

    total = 0

    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2

    return math.sqrt(total)


for iteration in range(max_iter):
    clusters = [[] for _ in range(K)]

    # clustering
    for idx, point in enumerate(data):
        distances = []

        for centroid in centroids:
            distances.append(
                euclidean_distance(point, centroid)
            )

        cluster_index = distances.index(min(distances))
        clusters[cluster_index].append(idx)

    # centroid baru
    new_centroids = []

    for cluster in clusters:
        centroid = []

        for i in range(len(data[0])):
            mean = sum(data[idx][i] for idx in cluster) / len(cluster)
            centroid.append(mean)

        new_centroids.append(centroid)

    # stop jika sama
    if new_centroids == centroids:
        break

    centroids = new_centroids

print("\nHASIL CLUSTER GEDUNG")

for i, cluster in enumerate(clusters):

    print(f"\nCluster {i+1}")

    for idx in cluster:
        print(nama_gedung[idx], "->", data[idx])

print("\nCENTROID AKHIR")

for i, centroid in enumerate(centroids):
    print(f"Cluster {i+1}: {centroid}")