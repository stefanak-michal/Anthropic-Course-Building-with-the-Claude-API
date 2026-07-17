param(
    [string]$Script = "chat.py"
)

docker run -it -v "${PWD}/src:/app" my-python-app $Script
