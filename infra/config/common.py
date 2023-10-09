from dataclasses import dataclass


@dataclass
class Environment:
    name: str
    account_id: str
    region: str
    backend_bucket: str


ENVIRONMENTS = {
    "DEV_VIRGINIA": Environment(
        name="dev",
        account_id="937168356724",
        region="us-east-1",
        backend_bucket="terraform-states-flat",
    ),
    "PROD_VIRGINIA": Environment(
        name="prod",
        account_id="937168356724",
        region="us-east-1",
        backend_bucket="terraform-states-flat",
    ),
}
