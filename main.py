from typing import Annotated
import typer
import pathlib
import hashlib

app = typer.Typer()

def scan(folder: str):
    p = pathlib.Path(folder)
    for f in p.rglob(f"*"):
        if f.is_file():
            try:
                h = hashlib.blake2b()
                with f.open('rb') as handle:
                    content = handle.read()
                    h.update(content)
                    print(h.hexdigest())
            except PermissionError :
                print(f"SKIPPING: {f.name} (Permission Denied)")

            except Exception as e:
                print(f"ERROR: Could not scan {f.name}: {e}")







@app.command()
def main(
    folder : Annotated[str,typer.Argument]
):
    if folder:
        scan(folder)
    

if __name__ == "__main__":
    app()
