def test_run():
    import os
    with open("pytest_test_out.txt", "w") as f:
        f.write("Pytest ran successfully!\n")
        f.write(f"Current working directory: {os.getcwd()}\n")
        try:
            f.write(f"Files in current directory: {os.listdir('.')}\n")
        except Exception as e:
            f.write(f"Error listing dir: {e}\n")
