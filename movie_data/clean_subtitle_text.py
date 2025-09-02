import json
import re 
res = []
with open("clean_top1_movie_data_with_subtitle.json", "r", encoding="utf-8") as f:
    all_data = json.load(f)
    for data in all_data:
        text = data["subtitle_text"]
        #pattern = r'^\s*\d*\s*\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s*$'
        # cleaned_lines = [line for line in text.splitlines() if not re.match(pattern, line)]
        # clean_text =  '\n'.join(cleaned_lines)
        clean_text = re.sub(r"\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n", "", text)
        data["subtitle_text"] = clean_text

    with open("clean_top1_movie_data_with_subtitle2.json", 'w') as f:
        json.dump(all_data, f)
print("finished clean")