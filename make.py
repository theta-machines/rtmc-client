#!/usr/bin/env python3

"""
    Original Author: Ryan Stracener

    This script handles building, testing, and deploying the aio-mgr package.
    For usage, read the HELP_MESSAGE variable below.
"""

import glob, os, shutil, subprocess, sys

BUILD_DIR = "dist"
HELP_MESSAGE = (
    "Usage: make.py <command>\n"
    "\n"
    "Commands:\n"
    "  init    Install all dependencies\n"
    "  build   Build the library\n"
    "  test    Run the test suite\n"
    "  deploy  Deploy the library to PyPI\n"
)

def init_command():
    # Define dependencies
    pip_dependencies = [
        "build",
        "pytest",
        "twine"
    ]
    
    for dep in pip_dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", dep])



def build_command():
    # Remove the current build directory
    if os.path.exists(BUILD_DIR) and os.path.isdir(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

    # Build the library
    subprocess.check_call([sys.executable, "-m", "build"])

    # Install the .whl file
    wheel = _get_single_path(".whl")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", wheel])



def test_command():
    subprocess.check_call([sys.executable, "-m", "pytest"])



def deploy_command():
    # Enforce a clean build before deploying
    build_command()

    # Enforce passing tests before deploying
    test_command()

    # Get the .whl and .tar.gz files
    wheel = _get_single_path(".whl")
    tar_gz = _get_single_path(".tar.gz")
    
    # Verify the .whl file's metadata
    subprocess.check_call([sys.executable, "-m", "twine", "check", wheel, tar_gz])

    # Upload to PyPI
    subprocess.check_call([sys.executable, "-m", "twine", "upload", wheel, tar_gz])



"""
    Helper function that looks for a single file of some type in the BUILD_DIR
    Returns a single path or calls sys.exit().
"""
def _get_single_path(filetype):
    # Find all .whl files in the build directory
    filepaths = glob.glob(os.path.join(BUILD_DIR, f"*{filetype}"))

    # Make sure only one .whl was found
    if len(filepaths) != 1:
        sys.exit(f"ERROR: Expected one {filetype} file, but found {len(filepaths)}")
    else:
        return filepaths[0]



if __name__ == "__main__":
    # Map commands to handler methods
    command_handlers = {
        "init": init_command,
        "build": build_command,
        "test": test_command,
        "deploy": deploy_command,
    }

    # Make sure script runs from correct directory
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

    # Make sure script is running in a venv
    if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
        sys.exit("ERROR: This script must be run from within a virtual environment.")

    # Parse argument to choose correct handler method
    try:
        command_handler = command_handlers[sys.argv[1]]
    except (IndexError, KeyError):
        sys.exit("ERROR: Incorrect usage.\n\n" + HELP_MESSAGE)

    # Invoke the correct handler method
    command_handler()
