from typing import Annotated
import typer  
import pathlib
import hashlib
from collections import defaultdict
import shutil
import signal
import sys
from loguru import logger


app = typer.Typer()
logger.add('janitor.log')

def graceful_shutdown(sig,frame):
    logger.warning("\n[!] Janitor is dropping his broom and leaving...")
    sys.exit(0)


def scan(folder: str,dry_run: bool = True):
    p = pathlib.Path(folder)
    usage_before = shutil.disk_usage(p)
    print(f"Total Disk Usage is:{usage_before.used}")
    hash_store = defaultdict(list)
    for f in p.rglob(f"*"):
        if f.is_file():
            try:
                logger.info(f"Scanning the file : {f.name}")
                h = hashlib.blake2b()
                with f.open('rb') as handle:
                    content = handle.read()
                    h.update(content)
                    file_hash = h.hexdigest()
                    #Mapping the file_hash as key and f as the value
                    hash_store[file_hash].append(f)
            except PermissionError :
                logger.error(f"Permission Denied for {f.name}")

            except Exception as e:
                logger.error(f"ERROR: Could not scan {f.name}: {e}")
                
    for key,value in hash_store.items():
        if len(value) > 1:
            logger.info("\n[!] Duplicate Group Found")
            short_hash = key[:8]
            logger.info(f"[Group: {short_hash}] Found duplicates:")
            for path in value[1:]:
                if dry_run:
                    logger.info(f"These Values will be Deleted -> : {path}")
                else:
                    path.unlink()
                    logger.success("The files {path} are Deleted")
            usage_after = shutil.disk_usage(p)
            logger.info(f"Total Disk Usage now is : {usage_after.used}")


signal.signal(signal.SIGINT,graceful_shutdown)

@app.command()
def main(
    folder : Annotated[str,typer.Argument],
    dry_run : Annotated[bool,typer.Option()] = True
):
   return scan(folder,dry_run)

if __name__ == "__main__":
    app()

