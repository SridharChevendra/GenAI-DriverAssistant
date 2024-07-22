# GenAI-DriverAssistant

Building a Digital Driver Assistant with Generative AI model.

Architecture Diagram 

## Getting Started
### Pre-requisites
* AWS Account setup
* Access to Amazon Bedrock Foundational model
 
#### Environment setup
#### 1. Clone GitRepo to local machine

Create a folder names "driverAssist"

```
mkdir driverAssist && cd driverAssit

```
Clone the GitRepo to your local machine.
```
git clone https://github.com/SridharChevendra/eventBridgeCodeBuild.git
cd eventBridgeCodeBuild
```
#### 2. AWS stack deployment
* Login to your AWS account
* Follow the steps in the reference to grant access to Amazon Bedrock foundational model
  - https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
    - Note: This demo uses Claude3 model.Ensure access is granted to Claude3 model.
* Go to AWS cloudformation service and create a new stack using "template.yaml" file

#### 3. Test API Gateway
* On cloudformatin resources tab, Refer the logical ID "Api". Click the corresponding Physicalid. it opens a url.
* Append /claims to the above url. Following is the output from the API gateway.
* Append /carinfo to the above url. Following is the output from the API gateway.

#### 4. Upload Lambda code

#### 5. Setup UI

#### 6. Cleanup


