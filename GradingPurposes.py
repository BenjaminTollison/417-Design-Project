import argparse
import os
import shutil
import stat
import subprocess
import sys


def CreateVenv(venv_dir="design_env"):
    """
    Creates a virtual environment and provides instructions to activate it.

    Args:
        venv_dir (str): Directory where the virtual environment will be created.
    """
    # Step 1: Create the virtual environment
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        print(f"Virtual environment created successfully in '{venv_dir}'!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        sys.exit(1)

    # Step 2: Set execute permissions for the activate script
    activate_script = (
        os.path.join(venv_dir, "bin", "activate")
        if os.name != "nt"
        else os.path.join(venv_dir, "Scripts", "activate.bat")
    )
    if os.path.exists(activate_script):
        os.chmod(activate_script, os.stat(activate_script).st_mode | stat.S_IXUSR)
        print(f"Granted execute permissions to '{activate_script}'")

    # Step 3: Provide activation instructions
    if os.name == "nt":  # Windows
        activation_command = f"{venv_dir}\\Scripts\\activate"
    else:  # macOS/Linux
        activation_command = f"source {venv_dir}/bin/activate"

    print(
        f"\nTo activate the virtual environment, run the following command in your terminal:\n"
    )
    print(f"    {activation_command}\n")
    # Prompt the user to confirm activation
    print(
        "After activating the virtual environment, rerun this script with the 'python3 GradingPurposes.py --setup-pip'"
    )
    sys.exit(0)  # Exit after providing instructions


def InstallRequiredPackages():
    requirements_file = "requirements.txt"

    # Check if the requirements file exists
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found.")
        sys.exit(1)

    # Run pip install -r requirements.txt
    try:
        subprocess.check_call(["py", "-m", "ensurepip", "--upgrade"])
        subprocess.check_call(["pip", "install", "-r", requirements_file])
        print("All requirements installed successfully!")
        try:
            subprocess.check_call(["python3", "-m", "ensurepip", "--upgrade"])
            subprocess.check_call(["pip", "install", "-r", requirements_file])
            print("All requirements installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during installation: {e}")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during installation: {e}")
        sys.exit(1)


def GenerateCompressorPlots():
    return None


def DeleteTempVenv(venv_dir="design_env"):
    """
    Deletes the specified virtual environment directory.

    Args:
        venv_dir (str): Directory where the virtual environment is located.
    """
    # Check if the directory exists
    if os.path.exists(venv_dir) and os.path.isdir(venv_dir):
        try:
            shutil.rmtree(venv_dir)  # Remove the directory and its contents
            print(f"Virtual environment '{venv_dir}' deleted successfully!")
        except Exception as e:
            print(f"Error deleting virtual environment: {e}")
    else:
        print(f"Virtual environment '{venv_dir}' does not exist or is not a directory.")


def main():
    parser = argparse.ArgumentParser(
        description="Run tasks with a virtual environment."
    )
    parser.add_argument(
        "--setup-env",
        action="store_true",
        help="Create the virtual environment and prompt user to install the required packages if required.",
    )
    parser.add_argument(
        "--setup-pip",
        action="store_true",
        help="Create the virtual environment and prompt user to install the required packages if required.",
    )
    parser.add_argument(
        "--compressor",
        action="store_true",
        help="Continue with package installation and other tasks.",
    )
    parser.add_argument(
        "--turbine",
        action="store_true",
        help="Continue with package installation and other tasks.",
    )
    parser.add_argument(
        "--delete-temp",
        action="store_true",
        help="Continue with package installation and other tasks.",
    )
    args = parser.parse_args()

    if args.setup_env:
        CreateVenv()  # Create the virtual environment and exit
    elif args.setup_pip:
        InstallRequiredPackages()  # Install required packages
    elif args.compressor:
        print("NotImplementedError")
        return NotImplementedError
    elif args.turbine:
        print("NotImplementedError")
        return NotImplementedError
    elif args.delete_temp:
        DeleteTempVenv()  # Delete the virtual environment
    else:
        print("Usage: python GradingPurposes.py --setup-env")
        print("OR")
        print("Usage: python GradingPurposes.py --setup-pip")
        print("OR")
        print("python GradingPurposes.py --compressor")
        print("OR")
        print("python GradingPurposes.py --turbine")
        print("OR")
        print("python GradingPurposes.py --delete-temp")
        sys.exit(1)


if __name__ == "__main__":
    main()
