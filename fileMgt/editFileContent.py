def update_text(original_text, text_changes):
    new_lines = []

    for count, line in enumerate(original_text.splitlines()):
        current_line_number = count + 1

        if current_line_number in text_changes:
            text_to_insert_lines = text_changes[current_line_number].splitlines()
            new_lines.extend(text_to_insert_lines)

        new_lines.append(line)

    new_text = "\n".join(new_lines)

    return new_text


def update_file(filename, text_changes):
    with open(filename, 'r') as _file:
        contents = _file.read()

    new_file_content = update_text(contents, text_changes)

    with open(filename, 'w') as f:
        f.write(new_file_content)
