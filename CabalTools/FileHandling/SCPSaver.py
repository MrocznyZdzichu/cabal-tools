class SCPSaver:
    def __init__(self):
        pass

    def save_scp_file(self, data, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:            
            for section in data:
                f.write('\n\n')
                section_name = section['section']
                entries = section['entries']

                if not entries:
                    continue

                headers = [k for k in entries[0].keys() if k != "RowIndex"]

                f.write(f"[{section_name}]\t" + '\t'.join(headers) + '\n')

                for entry in entries:
                    row = [str(entry["RowIndex"])]
                    for key in headers:
                        val = entry.get(key, '')
                        if val is None:
                            val = "<null>"
                        row.append(str(val))
                    f.write('\t'.join(row) + '\n')
