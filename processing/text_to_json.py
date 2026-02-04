def text_to_json(text, source="unknown"):
    return {
        "source": source,
        "length": len(text),
        "content": text
    }
