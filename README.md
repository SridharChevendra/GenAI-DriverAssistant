# GenAI-DriverAssistant

Building a Digital Driver Assistant with Generative AI model.

![Proposed Architecture](https://github.com/SridharChevendra/GenAI-DriverAssistant/blob/98adb77a0a9cd1d23c91c66731545ac32a847c4f/architecture/Digital%20Driver%20Assistant%20Architecture-GenAI_Incident%20management.jpg)

### Description
AI for initial incident assessment, damaged parts identification, cost estimation, and provider claim verification. This demonstrates the transformative potential of Generative AI in the roadside assistance and accident management industry, where timely service is crucial for customer satisfaction, retention, and brand loyalty.
## Getting Started
### Pre-requisites
* AWS Account setup
* Access to Amazon Bedrock Foundational model
* Sagemaker Studio
 
#### Environment setup
#### 1. Clone GitRepo to local machine

Create a folder names "driverAssist"

```
mkdir driverAssist && cd driverAssist

```
Clone the GitRepo to your local machine.
```
git clone https://github.com/SridharChevendra/GenAI-DriverAssistant.git
cd GenAI-DriverAssistant
```
#### 2. AWS stack deployment
* Login to your AWS account
* Follow the steps in the reference to grant access to the Amazon Bedrock foundational model
  - https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
    - Note: This demo uses Claude3 model.Ensure access is granted to Claude3 model.
* Go to AWS cloudformation service and create a new stack using "template.yaml" file

#### 3. Test API Gateway
* On the CloudFormation Resources tab, locate the logical ID "Api" and click the corresponding Physical ID to open the URL.
* Append **"/claims"** to the URL. if the output is **"Hello from Claims Lambda!"**, proceed to next.
* Append **"/carinfo"** to the URL. if the output is **"Hello from Carinfo Lambda!"**, proceed to next step to upload lambda code.

#### 4. Upload Lambda code

#### 5. Setup UI
* Login into your sagemaker studio. Go to Terminal
* Ensure role has access to the S3 bucket that created part of the stack.
* Install the following python modules
  ```
  pip install boto3
  pip install requests
  pip install vin-decoder-nhtsa
  pip install streamlist ==1.26.0
  ```
* Upload the file front_end_v7.py
* Start the UI
  ```
  streamlit run front_end_v7.py
  ```
![UI](https://github.com/SridharChevendra/GenAI-DriverAssistant/blob/9a56f81925c150a67897b04dedf8d0ef3f51879f/Builderspace.PNG)

#### 6. Access UI
* On the Sagemaker studio url copy until default/ and append proxy/8501/
  - Example:
    - ** "https://<xxxxx>.studio.us-east-1.sagemaker.aws/jupyter/default/" replace with
      ** "https://<xxxxx>.studio.us-east-1.sagemaker.aws/jupyter/default/proxy/8501/"
  

#### 7. Cleanup
* Go to Sagemaker studio terminal window. <Ctrl>+C to kill the front_end_v7.py
* Go to AWS console, cloudformation, and delete the stack.

