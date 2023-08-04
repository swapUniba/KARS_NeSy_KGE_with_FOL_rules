import traceback
from typing import Callable
from utils.arguments import KaleSettings
from utils.exceptions import KaleException, AmarException, ElliotException
from time import time

def forEachEmbeddingDimension(kaleSettings: KaleSettings, f: Callable[[KaleSettings, int], None]):
    tStart = time()

    statuses = {}

    def updateStatusWithError(e: BaseException, dim: int, msg: str):
        traceback.print_exc()
        statuses[dim] = (f"something went wrong while {msg}", e)

    for dim in kaleSettings.dims:
        tLoopStart = time()
        print(f"\nSTARTING ON DIMENSION {dim}:\n")

        try:
            f(kaleSettings, dim)
            statuses[dim] = ("each requested process was successfully completed", "no problems occurred")
            
            print(f"\nSUCCESSFULLY COMPLETED ALL OPERATIONS ON DIMENSION {dim}.")
        except KaleException as e:
            updateStatusWithError(e, dim, "learning the embeddings with KALE")
        except AmarException as e:
            updateStatusWithError(e, dim, "training the model with AMAR")
        except ElliotException as e:
            updateStatusWithError(e, dim, f"running an Elliot experiment")
        except KeyboardInterrupt as e:
            print("\nPROCESS WAS HALTED BY THE USER.\n")
            break
        except BaseException as e:
            updateStatusWithError(e, dim, "executing an unknown phase of the process")
        finally:
            tLoopEnd = time()
            print(f"Worked on dimension {dim} for {tLoopEnd - tLoopStart} seconds.")

    tEnd = time()
    print(f"Total time spent: {tEnd - tStart} seconds.\n")

    print("RESULTS:")

    for dim, (msg, e) in statuses.items():
        print(f"Dimension {dim} > {msg} ({e}).")