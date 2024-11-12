import concurrent.futures
from typing import List, Tuple, Dict, Callable


# Assuming FunctionType is a Callable type
def run_tasks_concurrently(task_list: List[Tuple[Callable, Tuple]]) -> Dict[Callable, any]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create future objects for each task by submitting function and args
        futures = {
            func: executor.submit(func, *args) for func, args in task_list
        }

        results = dict()

        # Process results as they complete
        for func, future in futures.items():
            try:
                result = future.result()
                results[func] = result
            except Exception as exc:
                print(f"Task generated an exception: {exc}")
    return results
    