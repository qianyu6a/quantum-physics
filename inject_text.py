import json, re

html_path = "D:/知识库/quantum-physics/static/index.html"
text_path = "D:/知识库/quantum-physics/expanded_text.json"

with open(text_path, 'r', encoding='utf-8') as f:
    texts = json.load(f)

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

count = 0
for concept_id, new_text in texts.items():
    for field in ['problem', 'insight', 'bigpic']:
        # Find the old text: field:'...',
        pattern = rf"({field}:')([^']*)(')"
        # Find the right concept's field (needs to be within the right concept block)
        parts = html.split(f"id:'{concept_id}'")
        if len(parts) < 2:
            print(f"SKIP {concept_id}.{field}: concept not found")
            continue
        
        # Find the field within this concept block
        block = parts[1].split("},")[0] if concept_id != "qc" else parts[1].split("}];")[0]
        match = re.search(pattern, block)
        if match:
            old = match.group(0)
            new = f"{field}:'{new_text[field]}'"
            html = html.replace(old, new, 1)
            count += 1
            print(f"✓ {concept_id}.{field}: {len(old)}→{len(new)} chars")
        else:
            print(f"✗ {concept_id}.{field}: pattern not found in block")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone: {count}/45 fields replaced")
