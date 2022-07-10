## API Usage:

  The Application load balancer sits on top of the kubernetes ingress controller that has ingress routing rules to redirect the traffic to the services in the "application" namespace, this namespace contains the deployment of flask-python via replacement.py and can be accessed via LB url:
  k8s-applicat-minimali-39da1c4581-164359810.us-east-1.elb.amazonaws.com
  
Open the postman application or a terminal(if using via Curl):

* Set the request method as "GET" and url "k8s-applicat-minimali-39da1c4581-164359810.us-east-1.elb.amazonaws.com/replacement"
* Set the header "Host" as "replacement-svc.application", here replacement-svc is the namespaced service for namespace application the host header enables   the alb to route the request to the correctly mapped host.
* Set the query parameter "input" with value as the string to be replaced with certain keywords.

<img width="1002" alt="image" src="https://user-images.githubusercontent.com/71400950/177881357-446d74ff-68c6-4d9b-ae6d-76a05ddc176c.png">


## Application Overview:

The application is written in python which leverages the flask framework to make host API methods, replacement.py has an app route for uri endpoints "/" and "/replacement":

* The "/" method returns a simple "hello" and is the default return.
* The "/replacement" method reads the "input" variable from the query parameters and uses that string to identify the Keywords that need to be replaced and   returns the modified string.

The application Dockerfile helps up to build an image and push it in the private ECR, that can then be pulled in by the worker nodes that have IAM permissions to read the repository contents.


## Architecture Overview:

Here we have used AWS manages service call Elastic Kubernetes cluster that manages a kuberntes control plane for us, the entire setup is launched in a custom vpc that has 4 subnets:

* eks-network-PrivateSubnet01, eks-network-PrivateSubnet02 : These subnets are multi AZ - us-east-1a and us-east-1b, they host the node groups of the         cluster which are further used to create NodePort service, deploy ingress controller and ingress and our multi AZ application (Current deployment type     has 2 pods on one node in an AZ and 1 pod in the other AZ. 
* eks-network-PublicSubnet01, eks-network-PublicSubnet01 : The public subnets are hosting the Applcation load balancer that gets deployed upon creating       ingress routing rules within our application namespace. The public subnet has NAT gateway that has routing rule to the private subnet for communication     and also enable the worker nodes to communicate with the cluster API endpoint.

![image](https://user-images.githubusercontent.com/71400950/178109813-b6676357-bd41-49ac-b39b-74942563a02b.png)


## Steps to creating the Stack and deploying the application:

* Create IAM role for the EKS service to create a cluster on your behalf; also create a role for the node group to have read access on ECR.
* Checkout the git main branch; navigate to the "Cloud Formation" service and create a stack, in the template upload [EKS Network Configuration](cloud-formation-templates/amazon-eks-vpc-private-subnets.yaml) template.
* Next create a new stack and upload [EKS Cluster and Node group](cloud-formation-templates/eks-template.yaml) template, attach the roles previously created and also the subnets with VPC to be used.
* Associate IAM OIDC provider to your cluster:
 eksctl utils associate-iam-oidc-provider \
    --region <region-code> \
    --cluster <your-cluster-name> \
    --approve
* Download IAM policy for ALB controller: curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.1/docs/install/iam_policy.json
* Create the IAM policy:
  aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam-policy.json
* Create a IAM role and ServiceAccount for the AWS Load Balancer controller, use the ARN from the step above:
  eksctl create iamserviceaccount \
  --cluster=<cluster-name> \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
  --override-existing-serviceaccounts \
  --region <region-code> \
  --approve
* Install Cert Manager: kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.5.3/cert-manager.yaml
* Next, build the docker image "docker build -t <repoName:tag> ." and push it to the ECR.
* Apply the helm chart in this repo: helm install --set name=replacement ./ --namespace application
* The application should be up and running.


## CI/CD Integration

The following repository is accessed by a Jenkins server hosted on Amazon EC2 instance and has a multibranch project configured.
If required we can scan the repository content from jenkins and run a build to build the image and push it to ECR.
The new image file name is referred to from the values.yaml file in the root directory of the git repo so that it picks up the name with which we intend to deploy the cluster.
