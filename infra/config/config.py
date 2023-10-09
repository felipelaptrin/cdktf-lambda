from stack import LambdaProps

lambda_props = {
    "dev": LambdaProps(),
    "prod": LambdaProps(
        lambda_memory_in_MB=700,
    ),
}
