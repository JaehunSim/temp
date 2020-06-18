def classify(number, clusters, distance):
    if not clusters:
        clusters.append({"cluster": [number],
                         "average": number})
        return clusters
    cluster_found = False
    for cluster_dict in clusters:
        cluster = cluster_dict["cluster"]
        cluster_length = len(cluster)
        average = cluster_dict["average"]
        if abs(average - number) <= distance:
            cluster.append(number)
            new_average = (average*cluster_length + number) / (cluster_length + 1)
            cluster_dict["average"] = new_average
            cluster_found = True
            break
    if not cluster_found:
        clusters.append({"cluster": [number],
                         "average": number})
    return clusters
    
numbers = [1.1, 1.4, 3, 10.1, 10.8, 1.5, 3.1]
distance = 1
clusters = []
for number in numbers:
    clusters = classify(number, clusters, distance)
    
for cluster_dict in clusters:
    print(cluster_dict["cluster"])
