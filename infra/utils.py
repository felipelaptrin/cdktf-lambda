import os

from config.common import ENVIRONMENTS, Environment


class MissingEnvironmentVariable(Exception):
    pass


def get_environment() -> Environment:
    env_var_name = "ENVIRONMENT_NAME"
    available_environments = [*ENVIRONMENTS]
    if os.getenv(env_var_name) in available_environments:
        return ENVIRONMENTS[os.getenv(env_var_name)]
    else:
        message = f"You MUST set the {env_var_name} environment variable."
        message += f"Available values are: {', '.join(available_environments)}."
        raise MissingEnvironmentVariable(message)


def get_stack_name(stack_name: str) -> str:
    environment = get_environment()
    return f"{environment.name}-{stack_name}-{environment.region}"


def get_stack_props(stack_props):
    environment = get_environment()
    return stack_props[environment.name]
