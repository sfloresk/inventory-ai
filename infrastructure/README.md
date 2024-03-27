#  Inventory AI infrastructure

This project contains source code and supporting files for a serverless application that you can deploy using the SAM CLI. It is supported only in [regions where Amazon Bedrock is available](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html)

## Enable access for Claude 3 Sonnet and Amazon Titan image

Follow the steps in [this guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) to enable access of the model "Claude 3 Sonnet" and "Titan Image Generator G1" in us-east-1. The access status of both models should be equals to "Access granted"

## Deploy API Gateway, Lambda function and Cognito user pool

The application uses several AWS resources, including a Lambda function, a Cognito user pool and an API Gateway. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build
sam deploy --guided 
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts. (You can use the default values)

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name. For example: inventory-ai-infrastructure
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment. This will be needed if you are planing to deploy the [web portal](../web-portal/README.md)

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used inventory-ai-infrastructure as the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name inventory-ai-infrastructure
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.
