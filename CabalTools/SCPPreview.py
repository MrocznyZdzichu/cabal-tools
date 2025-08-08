import pandas as pd
from IPython.display import display, HTML

class SCPPreview:
    def __init__(self, max_height=400, max_width=900):
        self.max_height = max_height
        self.max_width = max_width

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
        
    def _valid_filter(self, df, filter_key=None, filter_val=None, filter_operator=None):
        problem_found = 0

        passed_filter_params = [filter_key, filter_val, filter_operator]
        if any(v is not None for v in passed_filter_params) and not all(v is not None for v in passed_filter_params):
            problem_found += 1

        if filter_operator not in ('==', '>', '>=', '<=', '<', '!=', 'like', 'regex') and all(v is not None for v in passed_filter_params):
            problem_found += 1
        
        if all(x is not None for x in passed_filter_params) and filter_key not in df.columns:
            problem_found += 1

        return not bool(problem_found)

    def _filtering(self, df, columns=None, filter_key=None, filter_val=None, filter_operator=None):
        if not self._valid_filter(df, filter_key, filter_val, filter_operator):
            raise ValueError('Improper filtering conditions.')

        if filter_operator in ('==', '>', '>=', '<=', '<', '!+'):
            df = df.query(f"`{filter_key}` {filter_operator} @filter_val")
            
        elif filter_operator == 'like':
            df = df[df[filter_key].astype(str).str.contains(str(filter_val), case=False, na=False)]

        elif filter_operator == 'regex':
            df = df[df[filter_key].astype(str).str.match(str(filter_val), na=False)]

        if columns is not None:
            df = df[columns]

        return df

    def preview_skills(self, data, section_name, columns=None, filter_key=None, filter_val=None, filter_operator=None):
        entries = [x for x in data if x['section'] == 'SKill_Main'][0]['entries']
        display(HTML(f"<h3 style='color:#4CAF50'>{section_name}</h3>"))
        if not entries:
            display(HTML("<i>Brak danych</i>"))
            return
        
        df = pd.DataFrame(entries)
        df = self._filtering(df, columns, filter_key, filter_val, filter_operator)
        styled_df_html = self._stylish_df(df)._repr_html_()
        scroll_box = self._wrap_in_scrollbox(styled_df_html)
        
        display(HTML(scroll_box))
        return df