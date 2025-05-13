#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

# task configurations
TASKS = [
    {
        "name": "task1",
        "domain": "task1/domain.pddl",
        "problem": "task1/pfile1.pddl",
        "search": "astar(lmcut())"  # using a* with lmcut heuristic for optimal plans
    },
    {
        "name": "task2_typed",
        "domain": "task2_typed/domain.pddl",
        "problem": "task2_typed/pfile.pddl",
        "search": "astar(lmcut())"
    },
    {
        "name": "task3_cost",
        "domain": "task3_cost/domain.pddl",
        "problem": "task3_cost/prob.pddl",
        "search": "astar(lmcut())"  # good for cost-optimal planning
    },
    {
        "name": "task4",
        "domain": "task4/domain.pddl",
        "problem": "task4/prob.pddl",
        "search": "astar(lmcut())"  # good for cost-optimal planning with action costs
    }
]

# planning methods
METHODS = {
    "fd": {
        "name": "Fast Downward",
        "check_cmd": ["which", "fast-downward.py"],
        "install_info": [
            "Fast Downward planner not found.",
            "Please install Fast Downward:",
            "1. Clone repository: git clone https://github.com/aibasel/downward.git",
            "2. Build: cd downward && ./build.py",
            "3. Add to PATH: export PATH=$PATH:/path/to/downward"
        ]
    },
    "lapkt": {
        "name": "LAPKT",
        "check_cmd": ["which", "siw-then-bfsf"],
        "install_info": [
            "LAPKT planner not found.",
            "Please install LAPKT:",
            "1. Clone repository: git clone https://github.com/LAPKT-dev/LAPKT-public",
            "2. Follow installation instructions in the README"
        ]
    }
}

# lapkt planners to try
LAPKT_PLANNERS = [
    "siw-then-bfsf",  # iterated width followed by best-first
    "bfws",           # best-first width search
    "iw",             # iterative width
    "brfs"            # breadth-first search
]

def check_planner_exists(planner_method="fd"):
    """check if selected planner is installed"""
    # check for local fast-downward.py in current directory first
    if planner_method == "fd" and os.path.exists("./fast-downward.py"):
        print("using local fast-downward.py")
        return True
    
    try:
        subprocess.run(METHODS[planner_method]["check_cmd"], check=True, stdout=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        if planner_method == "lapkt":
            # try alternative lapkt planners
            for planner in LAPKT_PLANNERS:
                try:
                    subprocess.run(["which", planner], check=True, stdout=subprocess.PIPE)
                    # update the check command for future reference
                    METHODS["lapkt"]["check_cmd"] = ["which", planner]
                    return True
                except subprocess.CalledProcessError:
                    continue
        return False
    except KeyError:
        print(f"Unknown planner method: {planner_method}")
        return False

def install_planner(planner_method="fd"):
    """provide instructions to install planner"""
    # if we have a local fast-downward.py, build it
    if planner_method == "fd" and os.path.exists("./fast-downward.py"):
        print("local fast-downward.py found, building...")
        try:
            subprocess.run(["./build.py"], check=True)
            return
        except subprocess.CalledProcessError:
            print("error building fast-downward")
    
    for line in METHODS[planner_method]["install_info"]:
        print(line)
    sys.exit(1)

def generate_plan_fd(task):
    """generate optimal plan using fast downward"""
    name = task["name"]
    domain = task["domain"]
    problem = task["problem"]
    search = task["search"]
    
    print(f"\n--- Generating plan for {name} using Fast Downward ---")
    
    # ensure input files exist
    if not os.path.exists(domain):
        print(f"error: domain file {domain} not found")
        return False
    
    if not os.path.exists(problem):
        print(f"error: problem file {problem} not found")
        return False
    
    # create output directory
    output_dir = f"results/{name}/fd"
    os.makedirs(output_dir, exist_ok=True)
    
    # check if we should use local fast-downward.py
    fd_cmd = "fast-downward.py"
    if os.path.exists("./fast-downward.py"):
        fd_cmd = "./fast-downward.py"
    
    # run planner
    cmd = [
        fd_cmd, 
        "--plan-file", f"{output_dir}/plan.txt",
        domain, 
        problem, 
        "--search", search
    ]
    
    try:
        print(f"running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # save output
        with open(f"{output_dir}/output.txt", "w") as f:
            f.write(result.stdout)
        
        if result.returncode != 0:
            print(f"planner failed with exit code {result.returncode}")
            print(result.stderr)
            return False
        
        # check if plan was found
        if os.path.exists(f"{output_dir}/plan.txt"):
            with open(f"{output_dir}/plan.txt", "r") as f:
                plan = f.read()
            
            plan_length = len([line for line in plan.split("\n") if line and not line.startswith(";")])
            print(f"plan found with {plan_length} actions")
            return True
        else:
            print("no plan found")
            return False
            
    except Exception as e:
        print(f"error running planner: {e}")
        return False

def generate_plan_lapkt(task):
    """generate optimal plan using lapkt"""
    name = task["name"]
    domain = task["domain"]
    problem = task["problem"]
    
    print(f"\n--- Generating plan for {name} using LAPKT ---")
    
    # ensure input files exist
    if not os.path.exists(domain):
        print(f"error: domain file {domain} not found")
        return False
    
    if not os.path.exists(problem):
        print(f"error: problem file {problem} not found")
        return False
    
    # create output directory
    output_dir = f"results/{name}/lapkt"
    os.makedirs(output_dir, exist_ok=True)
    
    # get the appropriate lapkt planner
    lapkt_planner = METHODS["lapkt"]["check_cmd"][1]  # extract the planner command from check_cmd
    
    # check if this is a cost task
    is_cost_task = "cost" in name
    
    # set up planner command based on planner type and task type
    if lapkt_planner == "siw-then-bfsf":
        planner_cmd = [lapkt_planner, "--domain", domain, "--problem", problem, "--output", f"{output_dir}/plan.txt"]
        if is_cost_task:
            planner_cmd.append("--cost")
    elif lapkt_planner == "bfws":
        planner_cmd = [lapkt_planner, "--domain", domain, "--problem", problem, "--output", f"{output_dir}/plan.txt"]
        if is_cost_task:
            planner_cmd.extend(["--k-BFWS", "true"])
    elif lapkt_planner == "iw":
        planner_cmd = [lapkt_planner, "--domain", domain, "--problem", problem, "--output", f"{output_dir}/plan.txt"]
    else:  # generic command
        planner_cmd = [lapkt_planner, "--domain", domain, "--problem", problem, "--output", f"{output_dir}/plan.txt"]
    
    try:
        print(f"running command: {' '.join(planner_cmd)}")
        result = subprocess.run(planner_cmd, capture_output=True, text=True)
        
        # save output
        with open(f"{output_dir}/output.txt", "w") as f:
            f.write(result.stdout)
        
        if result.returncode != 0:
            print(f"planner failed with exit code {result.returncode}")
            print(result.stderr)
            return False
        
        # check if plan was found
        if os.path.exists(f"{output_dir}/plan.txt"):
            with open(f"{output_dir}/plan.txt", "r") as f:
                plan = f.read()
            
            plan_length = len([line for line in plan.split("\n") if line and not line.startswith(";")])
            print(f"plan found with {plan_length} actions")
            return True
        else:
            print("no plan found")
            return False
            
    except Exception as e:
        print(f"error running planner: {e}")
        return False

def generate_plan(task, method="fd"):
    """generate plan using specified method"""
    if method == "fd":
        return generate_plan_fd(task)
    elif method == "lapkt":
        return generate_plan_lapkt(task)
    else:
        print(f"unknown planning method: {method}")
        return False

def main():
    """main function to generate plans for all tasks"""
    import argparse
    
    # parse command line arguments
    parser = argparse.ArgumentParser(description="generate optimal plans for pddl tasks")
    parser.add_argument("--method", choices=["fd", "lapkt", "both"], default="fd",
                        help="planning method to use (default: fd)")
    args = parser.parse_args()
    
    methods = []
    if args.method == "both":
        methods = ["fd", "lapkt"]
    else:
        methods = [args.method]
    
    # check if planner is installed
    for method in methods:
        if not check_planner_exists(method):
            install_planner(method)
    
    # create results directory
    os.makedirs("results", exist_ok=True)
    
    # generate plans for all tasks
    for method in methods:
        success_count = 0
        print(f"\n=== Using {METHODS[method]['name']} planner ===")
        
        for task in TASKS:
            if generate_plan(task, method):
                success_count += 1
        
        print(f"\ncompleted: {success_count}/{len(TASKS)} plans generated successfully with {METHODS[method]['name']}")
    
if __name__ == "__main__":
    main()
