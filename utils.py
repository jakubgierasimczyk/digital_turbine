import plotly.express as px


# functions should not do two different things but this is just a POC

def data_size_by_category(data, column):
    ''' Check data size for each category in the `column`'''
    tmp = data.groupby([column], as_index=False).size()

    fig = px.bar(tmp, x=column, y='size',
                 title='Categories count')
    return tmp, fig


def target_column_distribution_per_category(data, column, target_column):
    ''' Plot boxplot of the `target_column` per each category in the `column`'''
    # only a sample of the data to be ploted; overview
    fig = px.box(data[[column, target_column]].sample(n=100_000, random_state=123),
                 x=column, y=target_column,
                 title=f'{target_column} distribution in each category')
    return fig


def categorical_column_check_wrapper(data, column, target_column, win_bid_cutoff=5):
    ''' Simple wrapper to run all function in one place'''
    _, fig = data_size_by_category(data, column)
    fig.show()

    fig = target_column_distribution_per_category(data, column, target_column)
    fig.show()

    fig = target_column_distribution_per_category(data.query(f'{target_column} <= {win_bid_cutoff}'), column, target_column)
    fig.show()


def get_top_categories(data, column, threshold=.9):
    ''' Select top categories from `columns` 
    Categories are taken until thier cumulative size reaches 90%, starting from biggest.
    '''
    tmp = data.groupby(column, as_index=False).size()
    tmp = tmp.sort_values(by='size', ascending=False)
    tmp['cumulative_sum'] = tmp['size'].cumsum()
    tmp['proportion'] = tmp['cumulative_sum'] / tmp['size'].sum()
    top_categories = list(
        tmp.query(f'proportion <= {threshold}')[column])
    return top_categories


def replace_rare_categories(data, column, top_categories_list, replace_with='OTHER'):
    ''' Given provided list of top categories, replace rare categories with 'OTHER' and
    keep 'big' categories unchanged
    '''
    updated = data[column].apply(
        lambda x: x if x in top_categories_list[column] else replace_with).\
            copy()
    return updated.astype('category')
