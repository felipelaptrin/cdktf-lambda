# CDKTF

This is a quick demo to test CDKTF as a tool to provision infrastructure in AWS.

## Code style
To standardize the code, the following packages are being used:
- **isort**: To organize/sort the imports of the python code
- **ruff**: To lint python code, i.e. checking for unused variabled, find potential errors, check code style violations...
- **black**: Automatically format the code. It is compatible with ruff.

### Local development
If you are using Visual Studio Code (or VSCodium) you can add to the `preferences.json` the following configuration:
```json
{
    "[python]": {
        "python.formatting.provider": "black",
        "python.formatting.blackPath": "black",
        "editor.formatOnSave": true,
        "editor.tabSize": 4,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
    }
}
```

## Infrastructure
The deployed in