def decode_metadata_text(text: str) -> dict:
    meta = {}
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() == '---':
            content_start = idx + 1
            break
        if ':' in line:
            key, val = line.split(':', 1)
            meta[key.strip().lower()] = val.strip()

    content = "\n".join(lines[content_start:]).lstrip()
    return {
        "topic":   meta.get("topic"),
        "title":   meta.get("title"),
        "grade":   meta.get("grade"),
        "content": content,
    }
