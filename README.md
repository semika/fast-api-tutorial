### Build Docker image
> docker build -t fast-api-tutorial:1.0 .

### Run docker image
> docker run --name fast-api-tutorial -p 8000:8000 -p 3306:3306 fast-api-tutorial:1.0

### Remove docker container
> docker container rm e106980b5830

### Deploying in K8s cluster
> kubectl apply -f quartz-scheduler-deployment.yml

### Undeploying
> kubectl delete -f quartz-scheduler-deployment.yml
> 
### Checkout the code

> git clone git@github.com-personal:semika/quartz-on-k8s.git

### Sharing code into git

.gitignore file should be as follows.

```
/.venv/*
.venv
__pycache__/

```

When you switch between two git accounts, you can set the origin URL as follows 

> git remote set-url origin git@github.com-personal:semika/aws-cognito.git

> git push origin master