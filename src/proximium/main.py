from uvicorn import run


def main():
    run("proximium.app:app", debug=True, reload=True)
