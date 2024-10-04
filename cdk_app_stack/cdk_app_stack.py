from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_apigateway as apigw,
    RemovalPolicy,
    Duration,
    CfnOutput
)
from constructs import Construct

class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM Role for Lambda Function
        lambda_role = iam.Role(self, "WesleyCdkAppRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="Wesley-cdk-app-role",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess")
            ]
        )

        # S3 Bucket
        bucket = s3.Bucket(self, "WesleyCdkAppBucket",
            bucket_name="wesley-cdk-app-bucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Lambda Function
        lambda_function = lambda_.Function(self, "WesleyCdkAppBackend",
            function_name="Wesley-cdk-app-backend",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("cdk_app_stack/lambda"),
            role=lambda_role,
            memory_size=512,
            timeout=Duration.minutes(1),
            environment={"BUCKET_NAME": bucket.bucket_name},
        )

         # API Gateway
        api = apigw.RestApi(self, "WesleyCdkAppApi",
            rest_api_name="Wesley-cdk-app-api",
            endpoint_types=[apigw.EndpointType.REGIONAL]
        )

        # Add file-upload resource with CORS enabled
        file_upload = api.root.add_resource("file-upload")
        file_upload.add_cors_preflight(
            allow_origins=["*"],  # You can restrict this to specific origins
            allow_methods=["POST", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"],
            max_age=Duration.days(1)
        )

        # Add POST method to file-upload resource with Lambda Proxy Integration
        file_upload.add_method("POST", 
            apigw.LambdaIntegration(
                lambda_function,
                proxy=True  # This enables Lambda Proxy Integration
            )
        )

        # Deploy the API to a 'prod' stage
        deployment = apigw.Deployment(self, "Deployment",
            api=api,
            description="Deployment for the API"
        )
        
        prod_stage = apigw.Stage(self, "ProdStage",
            deployment=deployment,
            stage_name="prod-test"
        )
        prod_stage.apply_removal_policy(RemovalPolicy.DESTROY)

        # Set the deployment stage as the default one for the API
        api.deployment_stage = prod_stage

        # Output the API URL
        CfnOutput(self, "ApiUrl",
            value=f"{api.url}file-upload",
            description="URL of the API Gateway"
        )

        # Integrate Lambda with API Gateway
        lambda_integration = apigw.LambdaIntegration(lambda_function)
