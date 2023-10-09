#!/usr/bin/env python
import os
from dataclasses import dataclass
from typing import Optional

from cdktf import AssetType, Fn, S3Backend, TerraformAsset, TerraformStack, Token
from cdktf_cdktf_provider_aws.iam_role import IamRole
from cdktf_cdktf_provider_aws.iam_role_policy_attachment import IamRolePolicyAttachment
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket
from cdktf_cdktf_provider_aws.s3_object import S3Object
from config.common import Environment
from constructs import Construct


@dataclass
class LambdaProps:
    lambda_name: Optional[str] = "dummy"
    lambda_memory_in_MB: Optional[int] = 512
    lambda_timeout_in_seconds: Optional[int] = 5


class LambdaStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, env: Environment, props: LambdaProps):
        super().__init__(scope, id)

        AwsProvider(self, "aws", region=env.region)
        S3Backend(
            self, region=env.region, bucket=env.backend_bucket, key="lambda.tfstate"
        )

        lambda_bucket = S3Bucket(
            self,
            f"{props.lambda_name}",
            bucket_prefix=props.lambda_name,
            force_destroy=True,
        )

        current_path = os.path.dirname(__file__)
        path_one_level_before = "/".join(current_path.split("/")[:-1])
        asset = TerraformAsset(
            self,
            f"{props.lambda_name}-lambda-asset",
            path=f"{path_one_level_before}/lambda",
            type=AssetType.ARCHIVE,
        )

        S3Object(
            self,
            f"{props.lambda_name}-lambda-object",
            bucket=lambda_bucket.bucket,
            key=asset.file_name,
            source=asset.path,
        )

        lambda_trust_relationship = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }

        lambda_role = IamRole(
            self,
            "lambda-role",
            name=props.lambda_name,
            assume_role_policy=Token.as_string(
                Fn.jsonencode(lambda_trust_relationship)
            ),
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            ],
        )

        LambdaFunction(
            self,
            "lambda",
            function_name=props.lambda_name,
            role=lambda_role.arn,
            architectures=["x86_64"],
            s3_bucket=lambda_bucket.bucket,
            s3_key=asset.file_name,
            package_type="Zip",
            handler="index.handler",
            runtime="nodejs18.x",
            memory_size=props.lambda_memory_in_MB,
            timeout=props.lambda_timeout_in_seconds,
            source_code_hash=Token.as_string(asset.asset_hash),
        )
