import sys

from zum.executor import Executor

if __name__ == "__main__":
    executor = Executor()
    executor.execute(sys.argv[1])
