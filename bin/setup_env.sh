python -m venv venv
activate() {
    . venv/bin/activate
    echo "installing requirements to the virtual environment"
    pip install -r requirements.txt
}
activate