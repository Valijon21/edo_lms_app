import subprocess

def run_cmd(args):
    res = subprocess.run(args, capture_output=True, text=True, timeout=15)
    return res.stdout, res.stderr, res.returncode

try:
    status_out, status_err, code = run_cmd(["git", "status"])
    log_out, log_err, log_code = run_cmd(["git", "--no-pager", "log", "-n", "3", "--oneline"])
    branch_out, branch_err, branch_code = run_cmd(["git", "branch", "-a"])
    
    with open("git_check_output.txt", "w", encoding="utf-8") as f:
        f.write("=== GIT STATUS ===\n")
        f.write(status_out)
        f.write(status_err)
        f.write(f"\nReturn Code: {code}\n\n")
        
        f.write("=== GIT LOG ===\n")
        f.write(log_out)
        f.write(log_err)
        f.write(f"\nReturn Code: {log_code}\n\n")
        
        f.write("=== GIT BRANCH ===\n")
        f.write(branch_out)
        f.write(branch_err)
        f.write(f"\nReturn Code: {branch_code}\n\n")
        
    print("Done writing git_check_output.txt")
except Exception as e:
    with open("git_check_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Exception: {e}\n")
    print("Error:", e)
