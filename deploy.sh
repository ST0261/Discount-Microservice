echo "Checking if docker is installed"
if ! [ -x "$(command -v docker)" ]; then
    echo "Install and start docker"
    yum update -y
    yum install -y docker
    service docker start
    usermod -a -G docker ec2-user
    echo "Done..."
else
    echo 'Docker is installed'
fi

docker image build -t discount-img .

docker stop discount-container
docker rm discount-container

docker run -d --name discount-container -p 80:5000 discount-img


