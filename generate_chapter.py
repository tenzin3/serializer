import json

def generate_chapters(num_chapters=10, segment_size=100):
    chapters = {}
    for i in range(1, num_chapters + 1):
        start = (i - 1) * segment_size + 1
        end = i * segment_size
        chapters[str(i)] = list(range(start, end + 1))
    
    return chapters

# Generate JSON structure
chapters_json = json.dumps(generate_chapters(), indent=2)

# Save to file
with open("chapter.json", "w") as f:
    f.write(chapters_json)

print("JSON file 'chapters.json' has been generated!")