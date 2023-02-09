% check existing containers
docker ps -a

% check existing images
docker images

% create container
docker run -d -it --name spiced python:3.7-slim

% quit container
ctrl+q 

% stop container
ctrl+c