import argparse, json, os
A, T, P, F = {}, {}, {}, "broker_state.json"
def S(): json.dump({'agents': A, 'tasks': T, 'p': P}, open(F, 'w'))
def R(a, c): return False if a in A else (A.update({a: {'capabilities': c, 'tasks': []}}) or S() or True)
def U(t, r): return False if t in T else (T.update({t: {'requirements': r, 'assigned_agents': []}}) or S() or True)
def Z(a, r): return 1.0 + sum(s/(s+f) for r_ in r if r_ in P.get(a, {}) for s, f in [P[a][r_]] if s+f > 0)
def Tf(a): return [] if a not in A else [t for t, _ in sorted([(t, Z(a, T[t]['requirements'])) for t in T if all(r in A[a]['capabilities'] for r in T[t]['requirements'])], key=lambda x: x[1], reverse=True)]
def Af(t): return [] if t not in T else [a for a, _ in sorted([(a, Z(a, T[t]['requirements'])) for a in A if all(r in A[a]['capabilities'] for r in T[t]['requirements'])], key=lambda x: x[1], reverse=True)]
def C(t, a, s=True):
    if a in A and t in T:
        ag, ta = A[a], T[t]
        [P.setdefault(a, {}).setdefault(r, [0, 0])[0 if s else 1] for r in ta['requirements'] if r in ag['capabilities']]
        S()
def ST(): return {'agent_count': len(A), 'task_count': len(T), 'agents': A, 'tasks': T}
def M():
    global A, T, P
    if os.path.exists(F): f = open(F); d = json.load(f); f.close(); A, T, P = d.get('agents', {}), d.get('tasks', {}), d.get('p', {})
    p = argparse.ArgumentParser(description="Adaptive Multi-Task Agent Coordinator")
    s = p.add_subparsers(dest='cmd', required=True)
    r = s.add_parser('register')
    r.add_argument('agent_id')
    r.add_argument('capabilities', nargs='+')
    u = s.add_parser('submit')
    u.add_argument('task_id')
    u.add_argument('requirements', nargs='+')
    m = s.add_parser('tasks')
    m.add_argument('agent_id')
    a_parser = s.add_parser('agents')
    a_parser.add_argument('task_id')
    c_parser = s.add_parser('complete')
    c_parser.add_argument('task_id')
    c_parser.add_argument('agent_id')
    c_parser.add_argument('--fail', action='store_true')
    s.add_parser('status')
    a_ = p.parse_args()
    cmds = {'register': lambda: (print(f"Registered {a_.agent_id}") if R(a_.agent_id, a_.capabilities) else None, S()), 'submit': lambda: (print(f"Submitted {a_.task_id}") if U(a_.task_id, a_.requirements) else None, S()), 'tasks': lambda: print("\n".join(Tf(a_.agent_id))), 'agents': lambda: print("\n".join(Af(a_.task_id))), 'complete': lambda: C(a_.task_id, a_.agent_id, not a_.fail), 'status': lambda: print(json.dumps(ST()))}
    cmds[a_.cmd]()
if __name__ == "__main__": M()
