echo "Running spectral clustering on red-blue-clusters.tab..."
python spectral.py ../datasets/red-blue-clusters.tab 3

echo "Running kmeans clustering on red-blue-clusters.tab..."
python kmeans.py ../datasets/red-blue-clusters.tab 2

echo "Running spectral clustering on circle-weird.tab..."
python spectral.py ../datasets/circle-weird.tab 3

echo "Running kmeans clustering on circle-weird.tab..."
python kmeans.py ../datasets/circle-weird.tab 2
