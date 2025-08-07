class SCPLoader:
    def __init__(self):
        pass

    def _parse_section_header(self, line):
        parts = line.split('\t')
        section_name = parts[0].strip()[1:-1]
        headers = parts[1:]  # nie zawiera indeksu!
        return section_name, headers

    def _parse_entry_line(self, line, headers):
        parts = line.split('\t')

        if len(parts) < len(headers) + 1:
            raise ValueError(f"Liczba kolumn ({len(parts)}) mniejsza niż liczba nagłówków + indeks ({len(headers)+1})")

        entry = {}

        # Pierwszy element to indeks — zapisujemy go osobno
        try:
            entry['RowIndex'] = int(parts[0])
        except ValueError:
            entry['RowIndex'] = parts[0]

        # Pozostałe elementy dopasowujemy do nagłówków
        for i in range(len(headers)):
            key = headers[i]
            val = parts[i + 1]

            if val == "<null>":
                val = None
            else:
                val = self._convert_value(val)

            entry[key] = val

        return entry

    def _convert_value(self, val):
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val

    def load_scp_file(self, scp_path):
        result = []
        current_section = None
        current_headers = []

        with open(scp_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith('[') and ']' in line:
                    section_name, current_headers = self._parse_section_header(line)
                    current_section = {
                        'section': section_name,
                        'entries': []
                    }
                    result.append(current_section)
                elif current_section is not None and current_headers:
                    entry = self._parse_entry_line(line, current_headers)
                    current_section['entries'].append(entry)

        return result
