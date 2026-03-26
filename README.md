# Adaptive Multi-Task Agent Coordinator

A lightweight CLI tool that extends the `AgentBroker` with dynamic, performance-based task adaptation. It matches agents to tasks not just by capability fit, but by historical success rates, enabling real-time optimization of assignments as the system learns.

## Features

- **Capability-based matching**: Core matching from `agent_representation_broker`
- **Performance tracking**: Records task completion outcomes (success/failure)
- **Adaptive scoring**: Prioritizes agents with proven success in required capabilities
- **CLI interface**: Simple commands for registration, submission, and querying

## Prerequisites

- Python 3.8+
- `agent_representation_broker` package installed (e.g., `pip install -e ../agent_representation_broker`)

## Usage

```bash
python3 main.py --help
```

### Commands

- `register <agent_id> <capabilities...>` – Register a new agent with space-separated capabilities.
- `submit <task_id> <requirements...>` – Submit a task with space-separated requirements.
- `tasks <agent_id>` – List task IDs that match the agent (scored by performance).
- `agents <task_id>` – List agent IDs that match the task (scored by performance).
- `complete <task_id> <agent_id> [--fail]` – Record a task completion outcome; defaults to success, use `--fail` to record failure.
- `status` – Print full broker state (agents, tasks, performance data) as JSON.

## Example Workflow

```bash
# Register two agents
python3 main.py register agent1 python debugging testing
python3 main.py register agent2 javascript frontend design

# Submit tasks
python3 main.py submit task1 python debugging
python3 main.py submit task2 javascript design

# See initial matches (equal scores)
python3 main.py tasks agent1
# Output: task1

python3 main.py agents task1
# Output: agent1

# Simulate task 1 completed successfully by agent1
python3 main.py complete task1 agent1

# Now agent1 will have a higher score for tasks requiring 'python' or 'debugging'
# Future matches prioritize agent1 for similar tasks over other agents with no history.
```

## Verification

To verify the tool is working correctly:

```bash
# Show help
python3 main.py --help

# Quick test
python3 main.py register tester python
python3 main.py submit test_task python
python3 main.py tasks tester
python3 main.py status
```

## How Adaptability Works

The `AdaptiveBroker` maintains a performance matrix `p[agent_id][capability] = [success_count, failure_count]`. When computing matches, the base score of 1.0 is augmented by the success rate for each required capability: `score += success_count / (success_count + failure_count)`. Agents with a history of successful completions in a capability receive a boost, while those with failures do not. This creates a self-reinforcing loop: effective agents get more tasks, generating more data to refine assignments.

The system updates in real-time: every call to `complete()` immediately affects subsequent match queries.

## Output

Commands return plain text lines (IDs) or JSON for `status`. This makes the tool script-friendly.
