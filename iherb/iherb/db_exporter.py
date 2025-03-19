
import pandas as pd

from iherb.iherb.items import session, db_path


def db_toexcel():
    with session:
        df = pd.DataFrame(pd.read_sql_table(table_name='product_4', con=db_path))
        df['URL'] = df['URL'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')
        df['Image_url'] = df['Image_url'].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')
        df.to_excel('Iherb_products.xlsx', index=False)
        df.to_csv(r'D:\Github\aprinur\scrapy_Iherb\iherb\iherb\Iherb_product.csv', index=False)
        print('Export finish')


if __name__ == '__main__':
    db_toexcel()