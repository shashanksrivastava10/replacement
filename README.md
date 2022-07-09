API Usage:

  The Application load balancer sits on top of the kubernetes ingress controller that has ingress routing rules to redirect the traffic to the services in the "application" namespace, this namespace contains the deployment of flask-python via replacement.py and can be accessed via LB url:
  k8s-applicat-minimali-39da1c4581-164359810.us-east-1.elb.amazonaws.com
  
Open the postman application or a terminal(if using via Curl):

* Set the request method as "GET" and url "k8s-applicat-minimali-39da1c4581-164359810.us-east-1.elb.amazonaws.com/replacement"
* Set the header "Host" as "replacement-svc.application", here replacement-svc is the namespaced service for namespace application the host header enables   the alb to route the request to the correctly mapped host.
* Set the query parameter "input" with value as the string to be replaced with certain keywords.

<img width="1002" alt="image" src="https://user-images.githubusercontent.com/71400950/177881357-446d74ff-68c6-4d9b-ae6d-76a05ddc176c.png">


Application Overview:

The application is written in python which leverages the flask framework to make host API methods, replacement.py has an app route for uri endpoints "/" and "/replacement":

* The "/" method returns a simple "hello" and is the default return.
* The "/replacement" method reads the "input" variable from the query parameters and uses that string to identify the Keywords that need to be replaced and   returns the modified string.

The application Dockerfile helps up to build an image and push it in the private ECR, that can then be pulled in by the worker nodes that have IAM permissions to read the repository contents.


Architecture Overview:

Here we have used AWS manages service call Elastic Kubernetes cluster that manages a kuberntes control plane for us, the entire setup is launched in a custom vpc that has 4 subnets:

* eks-network-PrivateSubnet01, eks-network-PrivateSubnet02 : These subnets are multi AZ - us-east-1a and us-east-1b, they host the node groups of the         cluster which are further used to create NodePort service, deploy ingress controller and ingress and our multi AZ application (Current deployment type     has 2 pods on one node in an AZ and 1 pod in the other AZ. 
* eks-network-PublicSubnet01, eks-network-PublicSubnet01 : The public subnets are hosting the Applcation load balancer that gets deployed upon creating       ingress routing rules within our application namespace. The public subnet has NAT gateway that has routing rule to the private subnet for communication     and also enable the worker nodes to communicate with the cluster API endpoint.

![image](https://user-images.githubusercontent.com/71400950/178109813-b6676357-bd41-49ac-b39b-74942563a02b.png)


