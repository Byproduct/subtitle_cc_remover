import os
import re

# remove CC lines from a file, returning tuple: a new file and removed CCs
def remove_cc_lines(input_file):
    CClines = []
    cleaned_text = []

    try:
        with open(input_file) as f:
            for line in f:
                line = line.rstrip()
                if len(line) > 2 and line.startswith(("[", "(")) and line.endswith(("]", ")")):
                    CClines.append(line)
                else:
                    cleaned_text.append(line)
    except:
        pass

    return cleaned_text, CClines


# rebuild subtitle file, discarding sections that are empty after removed CCs.
def rebuild_subtitles(input_text):
    rebuilt_index = 1
    subtitles = []

    for i in range(len(input_text)):
        # find timestamps (e.g. 00:00:05,380 --> 00:00:08,508)
        if re.search(r"\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d", input_text[i]):
            # after a timestamp is found, add lines to content until empty line is found
            # (empty line separates subtitles in .srt)
            j = i + 1
            subtitle_content = []
            if j < len(input_text) - 1:
                while input_text[j]:
                    subtitle_content.append(input_text[j])
                    j = j + 1
                    # break at the end of file to avoid index OOB
                    if j == len(input_text):
                        break
                if subtitle_content:
                    subtitle = {
                        "index": rebuilt_index,
                        "timestamp": input_text[i],
                        "content": subtitle_content
                    }
                    subtitles.append(subtitle)
                    rebuilt_index = rebuilt_index + 1

    rebuilt_text = []
    for subtitle in subtitles:
        rebuilt_text.append(str(subtitle["index"]))
        rebuilt_text.append(subtitle["timestamp"])
        for line in subtitle["content"]:
            rebuilt_text.append(line)
        rebuilt_text.append("\n")

    return rebuilt_text


def clean_single_file(input_file, output_file):
    if not input_file:
        return []
        
    cleaned_text, CClines = remove_cc_lines(input_file)

    # if no CC lines found in file, return empty list
    if not CClines:
        return []

    # if CC lines found, rebuild file
    rebuilt_text = rebuild_subtitles(cleaned_text)
    try:
        with open(output_file, "w") as f:
            for line in rebuilt_text:
                if "\n" in line:
                    f.write(line)
                else:
                    f.write(line + "\n")
        return CClines
    except:
        return []