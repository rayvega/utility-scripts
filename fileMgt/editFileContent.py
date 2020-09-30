def update_text(original_text, line_number, text_to_insert):
    new_lines = []

    text_to_insert_lines = text_to_insert.splitlines()

    for count, line in enumerate(original_text.splitlines()):
        current_line_number = count + 1

        if current_line_number == line_number:
            new_lines.extend(text_to_insert_lines)

        new_lines.append(line)

    new_text = "\n".join(new_lines)

    return new_text
