# Adaptive Multi-Task Agent Coordinator
import argparse, json, os
from agent_broker import AgentBroker
class AdaptiveBroker(AgentBroker):
    def __init__(s, f="broker_state.json"):
        super().__init__(); s.p = {}; s.f = f; s.load()
    def load(s):
        if os.path.exists(s.f):
            with open(s.f) as f: d = json.load(f)
            s.agents, s.tasks, s.p = d.get("agents", {}), d.get("tasks", {}), d.get("p", {})
    def save(s):
        with open(s.f, "w") as f: json.dump({"agents": s.agents, "tasks": s.tasks, "p": s.p}, f)
    def complete(s, tid, aid, succ=True):
        a, t = s.agents.get(aid), s.tasks.get(tid)
        if not a or not t: return
        for r in t["requirements"]:
            if r in a["capabilities"]:
                s.p.setdefault(aid, {}).setdefault(r, [0,0])[0 if succ else 1] += 1
        s.save()
    def _score(s, aid, reqs):
        sc = 1.0
        for r in reqs:
            if aid in s.p and r in s.p[aid]:
                suc, fail = s.p[aid][r]
                if suc+fail > 0: sc += suc/(suc+fail)
        return sc
    def get_matched_tasks(s, aid):
        if aid not in s.agents: return []
        caps = s.agents[aid]["capabilities"]
        return [tid for tid, _ in sorted([(tid, s._score(aid, t["requirements"])) for tid, t in s.tasks.items() if all(r in caps for r in t["requirements"])], key=lambda x: x[1], reverse=True)]
    def get_matched_agents(s, tid):
        if tid not in s.tasks: return []
        reqs = s.tasks[tid]["requirements"]
        return [aid for aid, _ in sorted([(aid, s._score(aid, reqs)) for aid, a in s.agents.items() if all(r in a["capabilities"] for r in reqs)], key=lambda x: x[1], reverse=True)]
def main():
    p = argparse.ArgumentParser(description="Adaptive Multi-Task Agent Coordinator")
    s = p.add_subparsers(dest="cmd", required=True); r = s.add_parser("register", help="Register agent"); r.add_argument("agent_id"); r.add_argument("capabilities", nargs="+")
    t = s.add_parser("submit", help="Submit task"); t.add_argument("task_id"); t.add_argument("requirements", nargs="+")
    m = s.add_parser("tasks", help="Tasks for agent"); m.add_argument("agent_id")
    a = s.add_parser("agents", help="Agents for task"); a.add_argument("task_id")
    c = s.add_parser("complete", help="Record completion"); c.add_argument("task_id"); c.add_argument("agent_id"); c.add_argument("--fail", action="store_true")
    s.add_parser("status", help="Show status")
    b = AdaptiveBroker(); x = p.parse_args()
    if x.cmd == "register": b.register_agent(x.agent_id, x.capabilities); b.save(); print(f"Registered {x.agent_id}")
    elif x.cmd == "submit": b.submit_task(x.task_id, x.requirements); b.save(); print(f"Submitted {x.task_id}")
    elif x.cmd == "tasks": print("\n".join(b.get_matched_tasks(x.agent_id)))
    elif x.cmd == "agents": print("\n".join(b.get_matched_agents(x.task_id)))
    elif x.cmd == "complete": b.complete(x.task_id, x.agent_id, not x.fail)
    elif x.cmd == "status": print(json.dumps(b.get_status()))
if __name__ == "__main__": main()
