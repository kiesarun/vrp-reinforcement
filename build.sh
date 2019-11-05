echo "Building image"

docker build -t kiesarun/vrp-reinforcement:latest .

echo "pushing image"

docker push kiesarun/vrp-reinforcement:latest
