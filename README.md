# SelfieLessActs
Selfie-Less Acts is a social media application designed to showcase and share pictures of selfless acts. Users can upload these images to the server and view them via an integrated mobile app. The server is accessed using RESTful API calls.

The project leverages Amazon Web Services (AWS) features such as EC2 instances, security groups, target groups, and an Elastic Load Balancer to build a robust infrastructure. Additionally, we developed a custom orchestrator engine to efficiently handle user requests. Key features of this project include:

Container Management: Containers can be manually started.
Load Balancing: Requests are distributed across containers using a round-robin algorithm for improved performance and reliability.
Fault Tolerance: Continuous health checks monitor the containers to ensure optimal functionality.
Scalability: The number of act containers automatically scales up or down based on traffic volume managed by the orchestrator.
This architecture ensures efficient, reliable, and scalable service delivery for the Selfie-Less Acts application.
