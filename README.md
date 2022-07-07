API Usage:

  The Application load balancer sits on top of the kubernetes ingress controller that has ingress routing rules to redirect the traffic to the services in the "application" namespace, this namespace contains the deployment of flask-python via replacement.py and can be accessed via LB url:
  k8s-applicat-minimali-39da1c4581-164359810.us-east-1.elb.amazonaws.com
  
Open the postman application or a terminal(if using via Curl):

* Set the request method as "GET" and url "k8s-applicat-minimali-39da1c4581-164359810.us-east-1.elb.amazonaws.com/replacement"
* Set the header "Host" as "replacement-svc.application", here replacement-svc is the namespaced service for namespace application the host header enables   the alb to route the request to the correctly mapped host.
* Set the query parameter "input" with value as the string to be replaced with certain keywords.

<img width="1002" alt="image" src="https://user-images.githubusercontent.com/71400950/177881357-446d74ff-68c6-4d9b-ae6d-76a05ddc176c.png">

Architecture Overview:

