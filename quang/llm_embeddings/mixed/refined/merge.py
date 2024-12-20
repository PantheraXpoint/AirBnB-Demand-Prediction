def merge_files(file1_path, file2_path, output_path):
    with open(file1_path, 'r', encoding='utf-8') as f1:
        content1 = f1.read().strip()
    with open(file2_path, 'r', encoding='utf-8') as f2:
        content2 = f2.read().strip()

    sections1 = [s.strip() for s in content1.split('----------------------------')]
    sections2 = [s.strip() for s in content2.split('--------------------------------------------------')]
    merged_sections = []

    for sec1, sec2 in zip(sections1, sections2):
        intro = sec2.split('\n')[0]
        
        # Get content from file2 (excluding beginning and assumption)
        file2_lines = sec2.split('\n')[1:]
        main_content = []
        assumption = ""
        
        for line in file2_lines:
            if line.startswith('Assume'):
                assumption = line
            else:
                main_content.append(line)
                
        file2_content = '\n'.join(main_content)
        
        # Get middle content from file1 (excluding beginning and Assume)
        file1_lines = sec1.split('\n')
        middle_content = '\n'.join(line for line in file1_lines[1:] 
                                 if not line.startswith('Assume'))
        
        # Combine with assumption at the end
        merged_section = f"{intro}\n{file2_content}\n{middle_content}\n{assumption}"
        merged_sections.append(merged_section)

    final_content = "\n----------------------------\n".join(merged_sections)

    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write(final_content)

# Example usage
file1_path = 'quang/llm_embeddings/prompts/new_prompts/listing_prompts_new.txt'
file2_path = 'quang/llm_embeddings/prompts/new_prompts/refined_prompts_new.txt'
output_path = 'quang/llm_embeddings/prompts/new_prompts/refined_listing_new.txt'
merge_files(file1_path, file2_path, output_path)