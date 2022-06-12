from matplotlib import pyplot as plt
import pickle


def plot_strikerates(strikerates, mse, df, title=None, filename=None, params=None):
        """plots strikerate data.
        
        Args:
            strikerates (dict): the strikerates to plot. should be a dict output by Analyst.calculate_strikerates().
            mse (float): the mean squared error to plot. should be a float output by Analyst.mean_squared_error().
        """
        if title is not None:
            plt.title(title)
        plt.plot([0, 1], [0, 1], color='grey', linestyle='--')

        mean_predictions = []
        strikerates_list = []
        volume = []
        for key, value in strikerates.items():
            if value['mean_prediction'] is not None:
                mean_predictions.append(value['mean_prediction'])

                lower_bound, upper_bound = (float(x) / 100 for x in key.split('-'))
                total = (len(df[(df['probability'] >= lower_bound) & (df['probability'] < upper_bound)]))
                percentage = (total / len(df))
                volume.append(percentage)

            if value['strikerate'] is not None:
                strikerates_list.append(value['strikerate'])
            

        plt.fill_between(mean_predictions, volume, color='red', alpha=0.25, label='volume distribution')
        plt.plot(mean_predictions, strikerates_list, color='green', linestyle='-', marker='.', label='strikerate')

        # include params below graph
        if params is not None:
            params_text = f'xG_past_games: {params[0]}\n'
            params_text += f'suppression_range: {params[1]}\n'
            params_text += f'conversion_range: {params[2]}\n'
            params_text += f'sup_con_past_games: {params[3]}\n'
            params_text += f'h_a_weight: {params[4]}\n'
            params_text += f'h_a_past_games: {params[5]}'
            plt.gcf().set_size_inches(15, 15)
            plt.annotate(params_text, (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=12)

        
        plt.xlabel('mean predictions')
        plt.ylabel('strikerate')
        plt.annotate('MSE: ' + str(mse), xy=(0.02, 0.8), xycoords='axes fraction', fontsize=16)
        plt.legend(fontsize=16)
        plt.grid(True)
        if filename is None:
            plt.show()
        else:
            plt.savefig(f'{filename}.png')
        plt.clf()


    
def plot_fxG_vs_goals(df, fxG_mse, title=None, filename=None, params=None):
    """plots fxG data.
    
    Args:
        df (DataFrame): the dataframe to plot. should be a dataframe output by Analyst.calculate_fxG_vs_goals().
    """
    if title is not None:
        plt.title(title)
    plt.scatter(df['fxG'], df['goals_scored'], color='green', marker='.', label='fxG vs goals', alpha=0.2)
    plt.xlabel('fxG')
    plt.ylabel('goals scored')
    plt.annotate('fxG MSE: ' + str(fxG_mse), xy=(0.02, 0.8), xycoords='axes fraction', fontsize=16)

    # include params below graph
    if params is not None:
        params_text = f'xG_past_games: {params[0]}\n'
        params_text += f'suppression_range: {params[1]}\n'
        params_text += f'conversion_range: {params[2]}\n'
        params_text += f'sup_con_past_games: {params[3]}\n'
        params_text += f'h_a_weight: {params[4]}\n'
        params_text += f'h_a_past_games: {params[5]}'
        plt.gcf().set_size_inches(15, 15)
        plt.annotate(params_text, (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=12)

    plt.grid(True)
    if filename is None:
        plt.show()
    else:
        plt.savefig(f'{filename}.png')
    plt.clf()