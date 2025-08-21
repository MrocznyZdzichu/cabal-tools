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
    
    # def _stylish_df(self, df):
    #     return df.style.set_table_styles(
    #             [{'selector': 'th', 'props': [('background-color', '#f4f4f4'),
    #                                          ('color', '#333'),
    #                                          ('font-weight', 'bold')]}]
    #         ).set_properties(**{'text-align': 'center'}).hide(axis='index')
        
    def _stylish_df(self, df):
        return (
            df.style
            .set_table_styles(
                [
                    {
                        'selector': 'th',
                        'props': [
                            ('background-color', '#f4f4f4'),
                            ('color', '#333'),
                            ('font-weight', 'bold'),
                            ('position', 'sticky'),
                            ('top', '0'),
                            ('z-index', '2')  # żeby nagłówki były nad komórkami
                        ]
                    }
                ]
            )
            .set_properties(**{'text-align': 'center'})
            .hide(axis='index')
        )

    # def _wrap_in_scrollbox(self, df_html):
    #     return f"""
    #     <div style="max-height:{self.max_height}px; max-width:{self.max_width}px;
    #                 overflow:auto; border:1px solid #ccc; padding:5px;">
    #         {df_html}
    #     </div>
    #     """
    def _wrap_in_scrollbox(self, df_html):
        return f"""
        <div style="max-height:{self.max_height}px; max-width:{self.max_width}px;
                    overflow-y:auto; overflow-x:auto; border:1px solid #ccc; padding:5px;
                    display:block;">
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