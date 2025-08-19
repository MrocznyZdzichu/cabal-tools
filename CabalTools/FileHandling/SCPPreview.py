import pandas as pd
from IPython.display import display, HTML

class SCPPreview:
    def __init__(self, max_height=550, max_width=1400):
        self.max_height = max_height
        self.max_width = max_width

    def _valid_filter(self, df, filter_key=None, filter_val=None, filter_operator=None):
        if filter_key is None or filter_val is None or filter_operator is None:
            return 'WARN: Incomplete filter parameters.'

        if filter_operator not in ('==', '>', '>=', '<=', '<', '!=', 'like', 'regex'):
            return f'WARN: Unsupported operator "{filter_operator}".'

        if filter_key not in df.columns:
            return f'WARN: Column "{filter_key}" not found in dataframe.'

        return None

    # def _valid_filter(self, df, filter_key=None, filter_val=None, filter_operator=None):
    #     warn_msg = None

    #     passed_filter_params = [filter_key, filter_val, filter_operator]
    #     if any(v is not None for v in passed_filter_params) and not all(v is not None for v in passed_filter_params):
    #         warn_msg = 'WARN: Not all required filtering parameters has been passed.'

    #     if filter_operator not in ('==', '>', '>=', '<=', '<', '!=', 'like', 'regex') and all(v is not None for v in passed_filter_params):
    #         warn_msg = 'WARN: Passed filtering operator not supported.'
        
    #     if all(x is not None for x in passed_filter_params) and filter_key not in df.columns:
    #         warn_msg = 'WARN: Passed key-column name is not in the data columns.'

    #     return warn_msg

    def _set_sections(self, section_name, data):
        if section_name and not isinstance(section_name, list):
            return [section_name]
        
        if isinstance(section_name, list) and all(name in [section['section'] for section in data] for name in section_name):
            return section_name 
        
        if not section_name:
            return [section['section'] for section in data]

    def _filtering(self, df, columns=None, filter_key=None, filter_val=None, filter_operator=None):
        if not isinstance(filter_key, (list, tuple)) and filter_key is not None:
            filter_key = [filter_key]
            filter_val = [filter_val]
            filter_operator = [filter_operator]

        if filter_key is None:
            filter_key, filter_val, filter_operator = [], [], []

        for k, v, op in zip(filter_key, filter_val, filter_operator):
            warn = self._valid_filter(df, k, v, op)
            if warn:
                print(warn, 'Filtering will be omitted for this condition.')
                continue

            if op in ('==', '>', '>=', '<=', '<', '!='):
                df = df.query(f"`{k}` {op} @v")
            elif op == 'like':
                df = df[df[k].astype(str).str.contains(str(v), case=False, na=False)]
            elif op == 'regex':
                df = df[df[k].astype(str).str.match(str(v), na=False)]

        if columns is not None:
            if isinstance(columns, str):
                columns = [columns]
            df = df[columns]

        return df

    # def _filtering(self, df, columns=None, filter_key=None, filter_val=None, filter_operator=None):
    #     warn = self._valid_filter(df, filter_key, filter_val, filter_operator)
    #     if warn:
    #         print(warn, 'Filtering will be omitted.')
    #         return df

    #     if filter_operator in ('==', '>', '>=', '<=', '<', '!+'):
    #         df = df.query(f"`{filter_key}` {filter_operator} @filter_val")
            
    #     elif filter_operator == 'like':
    #         df = df[df[filter_key].astype(str).str.contains(str(filter_val), case=False, na=False)]

    #     elif filter_operator == 'regex':
    #         df = df[df[filter_key].astype(str).str.match(str(filter_val), na=False)]

    #     if columns is not None:
    #         if isinstance(columns, str):
    #             columns = [columns]
    #         df = df[columns]

    #     return df
    
    def _stylish_df(self, df):
        return df.style.set_table_styles(
                [{'selector': 'th', 'props': [('background-color', '#f4f4f4'),
                                             ('color', '#333'),
                                             ('font-weight', 'bold')]}]
            ).set_properties(**{'text-align': 'center'}).hide(axis='index')
        
    def _wrap_in_scrollbox(self, df_html):
        return f"""
        <div style="max-height:{self.max_height}px; max-width:{self.max_width}px;
                    overflow:auto; border:1px solid #ccc; padding:5px;">
            {df_html}
        </div>
        """
        
    def preview(self, data, section_name=None, columns=None, filter_key=None, filter_val=None, filter_operator=None):
        sects = self._set_sections(section_name, data)
        for sect in sects:
            entries = [x for x in data if x['section'] == sect][0]['entries']
            display(HTML(f"<h3 style='color:#4CAF50'>{sect}</h3>"))
            if not entries:
                display(HTML("<i>Brak danych</i>"))
                return
            
            df = pd.DataFrame(entries)
            df = self._filtering(df, columns, filter_key, filter_val, filter_operator)
            styled_df_html = self._stylish_df(df)._repr_html_()
            scroll_box = self._wrap_in_scrollbox(styled_df_html)
            
            display(HTML(scroll_box))
        if section_name:
            return df