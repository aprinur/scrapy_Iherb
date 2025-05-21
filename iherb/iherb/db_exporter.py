import os.path

import pandas as pd

from items import session, db_path


def db_toexcel():

    downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    excel_path = os.path.join(downloads_dir, 'Iherb_products.xlsx')
    csv_path = os.path.join(downloads_dir, 'Iherb_products.csv')

    with session:
        df = pd.DataFrame(pd.read_sql_table(table_name='Iherb_Product_Information', con=db_path))

        df['URL'] = df['URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')
        df['Image_url'] = df['Image_url'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')

        df.to_excel(excel_path, index=False, excel_writer='openpyxl')
        df.to_csv(csv_path, index=False)

        print('Export finish')
