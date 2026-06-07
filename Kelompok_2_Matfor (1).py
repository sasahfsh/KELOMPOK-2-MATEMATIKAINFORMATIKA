import math

gedung = {
    "FPMIPA A": [4.4, 4.1, 4.4],
    "FPMIPA B": [4.4, 3.8, 3.9],
    "FPMIPA C": [4.1, 3.7, 3.6],
    "FPTI A": [4, 4, 4.3],
    "FPTI B": [3.3, 3.6, 3.6],
    "FPTI C": [3.3, 3.8, 3.5],
    "FPTI D": [5, 5, 5],
    "FIP Lama": [3.8, 2.8, 3],
    "FIP Baru": [4.0, 4.1, 4],
    "FPBS A": [4.2, 3.5, 3.5],
    "FPBS B": [4, 3.5, 3.6],
    "FPOK A": [3.8, 3.7, 3.5],
    "Kolam Renang": [3, 3.5, 3.2],
    "Gymnasium": [3.5, 3.7, 3.5],
    "Sports Hall": [3.6, 3.6, 3.7]
}

K = 3
max_iter = 100

# ubah ke list
nama_gedung = list(gedung.keys())
data = list(gedung.values())

centroids = [
    gedung["FPTI A"],
    gedung["FPMIPA C"],
    gedung ["Kolam Renang"]
]

def euclidean_distance(a, b):

    total = 0

    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2

    return math.sqrt(total)


for iteration in range(max_iter):

    print(f"\n===== ITERASI {iteration + 1} =====")

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

    print("Cluster sementara:")

    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1}:")
        for idx in cluster:
            print(" ", nama_gedung[idx])

    # centroid baru
    new_centroids = []

    for cluster in clusters:
        centroid = []

        for i in range(len(data[0])):
            mean = sum(data[idx][i] for idx in cluster) / len(cluster)
            centroid.append(mean)

        new_centroids.append(centroid)

    print("\nCentroid baru:")
    for i, centroid in enumerate(new_centroids):
        print(f"Cluster {i+1}: {centroid}")

    if new_centroids == centroids:
        print("\nKonvergen! Proses berhenti.")
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

wcss = 0

for i, cluster in enumerate(clusters):

    centroid = centroids[i]

    for idx in cluster:

        distance = euclidean_distance(data[idx], centroid)
        wcss += distance ** 2

print("WCSS =", round(wcss, 4))

labels = [0] * len(data)

for cluster_id, cluster in enumerate(clusters):
    for idx in cluster:
        labels[idx] = cluster_id

silhouette_scores = []

for i in range(len(data)):

    current_cluster = labels[i]

    # a(i) = rata-rata jarak ke anggota cluster yang sama
    same_cluster = [
        idx for idx in clusters[current_cluster]
        if idx != i
    ]

    if len(same_cluster) == 0:
        a = 0
    else:
        a = sum(
            euclidean_distance(data[i], data[idx])
            for idx in same_cluster
        ) / len(same_cluster)

    # b(i) = rata-rata jarak ke cluster lain terdekat
    b = float('inf')

    for other_cluster in range(K):

        if other_cluster == current_cluster:
            continue

        distances = [
            euclidean_distance(data[i], data[idx])
            for idx in clusters[other_cluster]
        ]

        avg_distance = sum(distances) / len(distances)

        if avg_distance < b:
            b = avg_distance

    # jika cluster hanya berisi 1 anggota
    if max(a, b) == 0:
        s = 0
    else:
        s = (b - a) / max(a, b)

    silhouette_scores.append(s)

# silhouette keseluruhan
silhouette = sum(silhouette_scores) / len(silhouette_scores)

print("\nSILHOUETTE SCORE")
print("Nilai keseluruhan =", round(silhouette, 4))

# silhouette per cluster
print("\nSILHOUETTE PER CLUSTER")

for cluster_id, cluster in enumerate(clusters):

    total = 0

    for idx in cluster:
        total += silhouette_scores[idx]

    cluster_score = total / len(cluster)

    print(f"Cluster {cluster_id + 1}: {cluster_score:.4f}")
