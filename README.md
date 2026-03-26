# Adaptive Multi-Task Agent Coordinator

A self-contained CLI tool that matches agents with tasks using dynamic, performance-based scoring. The coordinator learns from task completion outcomes (success/failure) to prioritize better agent-task assignments over time. All data persists in `broker_state.json`.

## Features
- Register agents with capabilities
- Submit tasks with requirements
- Get sorted list of tasks for an agent based on historical performance
- Get sorted list of agents for a task based on success rates
- Record task completion (success or failure) to improve future matching
- No external dependencies beyond Python standard library

## Matching Algorithm

The score for an agent on a requirement is:

- Base score: 1.0
- Plus the agent's success rate for that capability (successes / total attempts), if history exists

Agents are sorted by descending score, so those with proven success on required capabilities appear first.

## Usage

```bash
python3 main.py --help
python3 main.py <command> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `register <agent_id> <capabilities...>` | Register a new agent with capabilities |
| `submit <task_id> <requirements...>` | Submit a new task with requirements |
| `tasks <agent_id>` | List tasks matching agent's capabilities, sorted by performance score |
| `agents <task_id>` | List agents matching task's requirements, sorted by performance score |
| `complete <task_id> <agent_id> [--fail]` | Record task completion; success by default, use `--fail` for failure |
| `status` | Show full state as JSON |

## Examples

```bash
# Register agents with capabilities
python3 main.py register alice python testing
python3 main.py register bob javascript

# Submit tasks
python3 main.py submit job1 python testing
python3 main.py submit job2 javascript

# Find tasks for alice (sorted by match quality)
python3 main.py tasks alice

# Find agents for job1 (sorted by match quality)
python3 main.py agents job1

# Record successful completion
python3 main.py complete job1 alice

# Record a failure instead
python3 main.py complete job1 alice --fail

# View full broker state
python3 main.py status
```

## State Persistence

All registrations, submissions, and performance history are saved automatically to `broker_state.json`. The tool loads this file on startup, enabling continuous operation across multiple runs.

## Verification

```bash
python3 main.py --help
python3 main.py register test_agent python
python3 main.py submit test_task python
python3 main.py status
```
