def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_merged_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def merge_reports(file1, file2):
    # Read both files
    text1 = read_file(file1)
    text2 = read_file(file2)
    
    # Split files by the separator
    reports1 = text1.split('----------------------------')
    reports2 = text2.split('--------------------------------------------------')
    
    # Remove empty strings and strip whitespace
    reports1 = [r.strip() for r in reports1 if r.strip()]
    reports2 = [r.strip() for r in reports2 if r.strip()]
    
    # Merge corresponding reports
    merged_reports = []
    for r1, r2 in zip(reports1, reports2):
        # Extract the introductory sentence from r1
        intro_line = r1.split('\n')[0]
        # Remove the intro line from r1
        remaining_r1 = '\n'.join(r1.split('\n')[1:])
        # Combine in desired order
        merged_reports.append(f"{intro_line}\n\n{r2}\n\n{remaining_r1}")
    
    # Join with separators
    final_text = '\n\n--------------------------------------------------\n\n'.join(merged_reports)
    
    return final_text

# Execute the merge
merged_content = merge_reports('quang/llm_embeddings/prompts/new_prompts/listing_prompts_new.txt', 'quang/llm_embeddings/prompts/new_prompts/raw_prompts_new.txt')
write_merged_file('quang/llm_embeddings/prompts/new_prompts/raw_listing_new.txt', merged_content)