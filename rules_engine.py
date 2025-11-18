
from collections import defaultdict

categories = ['Network', 'Hardware', 'Software', 'Access', 'Other']

keyword_rules = {
    'Network': ['internet', 'wifi', 'vpn', 'latency', 'connect', 'network'],
    'Hardware': ['laptop', 'printer', 'disk', 'server', 'blue screen', 'powering on', 'jammed'],
    'Software': ['application', 'error 500', 'crash', 'client', 'save changes', 'sync', 'email client'],
    'Access': ['login', 'password', 'permission', 'account locked', 'access to', 'password reset']
}

dept_rules = {
    'Finance': ['Access'],
    'HR': ['Access'],
    'Engineering': ['Network', 'Hardware', 'Software'],
    'Support': ['Software', 'Hardware', 'Network']
}


def predict_rule_based(description, department):
    """Applies keyword + department-based rules to classify IT incidents."""
    desc = description.lower()
    scores = defaultdict(int)

    # Keyword-based rule
    for cat, keywords in keyword_rules.items():
        for kw in keywords:
            if kw in desc:
                scores[cat] += 1

    # Department-based hints
    if department in dept_rules:
        for hint in dept_rules[department]:
            scores[hint] += 0.5

    # Get top match
    if scores:
        max_score = max(scores.values())
        if max_score == 0:
            return 'Other'
        candidates = [c for c, s in scores.items() if s == max_score]
        for c in categories:
            if c in candidates:
                return c
    return 'Other'
