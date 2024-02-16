"""Top-level package for lnxmanager"""

__app_name__ = "lnxmanager"
__version__ = "0.1.0"

(
    SUCCESS,
    PATH_ERROR,
    FLAG_ERROR
) = range(3)

ERRORS = {
    PATH_ERROR: "Path doesn't reachable",
    FLAG_ERROR: "There is no such flag"
}