#!/usr/bin/env python
from cdktf import App
from config.config import lambda_props
from stack import LambdaStack
from utils import get_environment, get_stack_name, get_stack_props

environment = get_environment()

app = App()

LambdaStack(app, get_stack_name("lambda"), environment, get_stack_props(lambda_props))

app.synth()
