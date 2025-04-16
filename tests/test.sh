#!/bin/bash
# Run the container in detached mode with a published port.
container_id=$(docker run -d -p 8080:80 my-test-website:latest)

# Allow some time for the container to start.
sleep 5

# Check for the expected text in the homepage.
response=$(curl -s http://localhost:8080)
if [[ "$response" == *"welcome to my test website"* ]]; then
  echo "Test passed: Site content is correct."
  ret=0
else
  echo "Test failed: Site content is not correct."
  ret=1
fi

# Stop the container.
docker stop $container_id
exit $ret
