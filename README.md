### Quick Start Guide ###
Navigate to cdk-app directory:

    cd .\transport-tribe-dakota\spike\TRAN-1106\cdk_app

Activate the Python virtual environment

    Python –m venv .venv 

    ./source .venv/bin/activate

Install Dependencies Python: 

    python -m pip install -r requirements.txt

Login to AWS Training account with AdministatorAccess

    aws sso login

Deploy the App to the active AWS account (AWS Training)

    cdk bootstrap

    cdk deploy

### HOUSEKEEPING ####
Only use Met Office AWS Training account


# Uploading Text Files to S3 Bucket Using App 
Option 1: Implement an existing frontend solution:
https://github.com/wesleyrichardson/TRAN1106-React-Frontend


Option 2: Engineer a new frontend solution:

Once cdk deploy is successfully run, the API gateway PROD endpoint will be printed.

Use this endpoint/file-upload as the POST target to upload text files.

Send a POST request to the API-Gateway Endpoint. 
POST data should take the form of a JavaScript FormData object with three elements:
(String message, String fileName, fileObject file)

    const formData = new FormData();
            formData.append("demo file", this.state.selectedFile, this.state.selectedFile.name);

    axios.post(this.state.postTarget, formData)

Example Endpoint: https://rmg4prq7c6.execute-api.eu-west-2.amazonaws.com/prod-test/file-upload