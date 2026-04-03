from typing import Annotated
import typer  
import pathlib
import hashlib
from collections import defaultdict


app = typer.Typer()

def scan(folder: str,dry_run: bool = True):
    p = pathlib.Path(folder)
    hash_store = defaultdict(list)
    for f in p.rglob(f"*"):
        if f.is_file():
            try:
                h = hashlib.blake2b()
                with f.open('rb') as handle:
                    content = handle.read()
                    h.update(content)
                    file_hash = h.hexdigest()
                    #Mapping the file_hash as key and f as the value
                    hash_store[file_hash].append(f)
            except PermissionError :
                print(f"SKIPPING: {f.name} (Permission Denied)")

            except Exception as e:
                print(f"ERROR: Could not scan {f.name}: {e}")
    
    for key,value in hash_store.items():
        if len(value) > 1:
            print(f"\n[!] Duplicate Group Found")
            print(f"Duplicates found for the key: {key}")
            for path in value[1:]:
                if dry_run:
                    print(f"These Values will be Deleted -> : {path}")
                else:
                    path.unlink()
                    print(f"Deleted{path}")  
                    

                    








@app.command()
def main(
    folder : Annotated[str,typer.Argument],
    dry_run : Annotated[bool,typer.Option()] = True
):
   return scan(folder,dry_run)

if __name__ == "__main__":
    app()

