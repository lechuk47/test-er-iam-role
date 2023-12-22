#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.iam_role import IamRole, IamRoleInlinePolicy
import os
import json

from input import AppInterfaceInput, parse_input
from typing import Any
from pathlib import Path

class Stack(TerraformStack):

    def check_env(self) -> None:
        if "INPUT" not in os.environ:
            raise Exception("Input not present")

        # Credentials are mounted via a Secret
        credentials = Path("/credentials")
        if not Path.is_file(credentials):
            raise Exception("No Credentials set for AWS")



    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.check_env()
        # Read the input
        input: AppInterfaceInput = parse_input(os.environ["INPUT"])

        AwsProvider(self, "Aws", region="us-east-1", shared_credentials_files=["/credentials"])

        assume_role_policy:dict[str, Any] = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": f"sts:{input.resource.assume_action}",
                    "Effect": "Allow",
                    "Principal": input.resource.assume_role.model_dump(by_alias=True, exclude_none=True)
                }
            ]
        }
        if input.resource.assume_condition:
            assume_role_policy["Statement"][0]["Condition"] = json.loads(input.resource.assume_condition)

        if input.resource.inline_policy:
            inline_policy = [IamRoleInlinePolicy(name=input.resource.identifier, policy=input.resource.inline_policy)]
        else:
            inline_policy = None

        iam_role = IamRole(
            self,
            input.resource.identifier,
            name=input.resource.identifier,
            assume_role_policy=json.dumps(assume_role_policy),
            inline_policy=inline_policy
        )

        TerraformOutput(self, input.resource.identifier + "_role_arn", value=iam_role.arn)

app = App()
Stack(app, "CDKTF")
app.synth()
