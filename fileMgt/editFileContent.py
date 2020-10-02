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
