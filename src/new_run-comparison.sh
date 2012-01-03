echo red-blue-clusters > result

echo "Running ECMC clustering on red-blue-clusters.tab..."
python new_ECMC.py ../datasets/red-blue-clusters.tab 0.2

echo "Running GMM clustering on red-blue-clusters.tab..."
python new_GMM.py ../datasets/red-blue-clusters.tab 2

echo "Running spectral clustering on red-blue-clusters.tab..."
python new_spectral.py ../datasets/red-blue-clusters.tab 3

echo "Running kmeans clustering on red-blue-clusters.tab..."
python new_kmeans.py ../datasets/red-blue-clusters.tab 2

echo "Running DBSCAN clustering on red-blue-clusters.tab..."
python new_DBSCAN.py ../datasets/red-blue-clusters.tab 0.05 7

echo circle-weird >> result


echo "Running ECMC clustering on circle-weird.tab..."
python new_ECMC.py ../datasets/circle-weird.tab 0.2

echo "Running GMM clustering on circle-weird.tab..."
python new_GMM.py ../datasets/circle-weird.tab 2

echo "Running spectral clustering on circle-weird.tab..."
python new_spectral.py ../datasets/circle-weird.tab 3

echo "Running kmeans clustering on circle-weird.tab..."
python new_kmeans.py ../datasets/circle-weird.tab 2

echo "Running DBSCAN clustering on circle-weird.tab..."
python new_DBSCAN.py ../datasets/circle-weird.tab 0.05 7

echo half-moons >> result


echo "Running ECMC clustering on half-moons.tab..."
python new_ECMC.py ../datasets/half-moons.tab 0.2

echo "Running GMM clustering on half-moons.tab..."
python new_GMM.py ../datasets/half-moons.tab 2

echo "Running spectral clustering on half-moons.tab..."
python new_spectral.py ../datasets/half-moons.tab 3

echo "Running kmeans clustering on half-moons.tab..."
python new_kmeans.py ../datasets/half-moons.tab 2

echo "Running DBSCAN on half-moons.tab..."
python new_DBSCAN.py ../datasets/half-moons.tab 0.05 7