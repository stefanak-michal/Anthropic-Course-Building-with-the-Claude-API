param(
    [string]$Script = "chat.py"
)

docker run -it --rm -v "${PWD}/src:/app" my-python-app $Script
