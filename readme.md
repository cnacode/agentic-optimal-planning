# Multi-Agent PDDL Plan Generator

This project provides a multi-agent system for generating, reviewing, and translating plans based on PDDL (Planning Domain Definition Language) domain and problem files. The system leverages multiple agents to ensure the generation of valid and optimal plans, as well as their translation into PDDL syntax.

## Features

1. **Plan Generation**: Generates a plan in plain English based on the provided PDDL domain and problem files.
2. **Plan Review**: Reviews the generated plan for validity and optimality.
3. **PDDL Translation**: Translates the reviewed plan into PDDL syntax.
4. **Supervisor Agent**: Manages the workflow by coordinating tasks between the agents.

## Workflow

1. **Input**: Provide PDDL domain and problem files.
2. **Plan Generation**: The `plan_generator` agent generates a plan in plain English.
3. **Plan Review**: The `plan_reviewer` agent validates the plan and checks its optimality.
4. **PDDL Translation**: The `pddl_translator` agent translates the plan into PDDL syntax.
5. **Supervisor**: The `supervisor` agent orchestrates the entire process, ensuring tasks are completed sequentially.

## How to Use

1. Place your PDDL domain and problem files in the appropriate directories (e.g., `task1/`, `task2_typed/`, etc.).
2. Run the `generate_plan_multi_agent.py` script to start the workflow.
3. The script will process each task and output the results.

## Example

The script processes the following tasks:

- **Task 1**: `task1/domain.pddl` and `task1/pfile1.pddl`
- **Task 2**: `task2_typed/domain.pddl` and `task2_typed/pfile.pddl`
- **Task 3**: `task3_cost/domain.pddl` and `task3_cost/prob.pddl`
- **Task 4**: `task4/domain.pddl` and `task4/prob.pddl`

## Dependencies

- `langchain_openai`
- `langchain_core`
- `langchain_groq`
- `langgraph`
- `llm_config`
- `utils`

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## File Structure

- `generate_plan_multi_agent.py`: Main script for the multi-agent workflow.
- `task1/`, `task2_typed/`, `task3_cost/`, `task4/`: Directories containing PDDL files for different tasks.
- `utils.py`: Utility functions for reading PDDL files and printing messages.

## Output

The script outputs the final message history for each task, including the generated plan, review results, and PDDL translation.

## License

This project is licensed under the MIT License. See `LICENSE.md` for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

# Outputs:
Task 1
; PDDL Plan
0: (fly plane1 city0 city1 fl1 fl0)


Task 2
; PDDL Plan
0. (pick-up D)
1. (stack D C)
2. (pick-up C)
3. (stack C B)
4. (pick-up B)
5. (stack B A)

Task 3
; PDDL Plan
0.001: (pick-up D)
0.002: (stack D C)
0.003: (pick-up C)
0.004: (stack C B)
0.005: (pick-up B)
0.006: (stack B A)


Task 4
; PDDL Plan
; Plan for problem: travel-to-airport
; Domain: travel-planning
; Cost: 6
0: (take-bus-to-terminal home bus-terminal) [1]
1: (take-bus-to-airport bus-terminal airport) [1]
2: (walk-to-security airport security) [1]
3: (go-through-security security post-security) [1]
4: (walk-to-gate post-security gate) [1]
5: (board-flight gate) [1]
