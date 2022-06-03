from matplotlib import pyplot as plt
import pickle


def plot(strikerates, mse, df, title=None, filename=None):
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
        
        plt.xlabel('mean predictions')
        plt.ylabel('strikerate')
        plt.annotate('wMSE (x100): ' + str(mse), xy=(0.02, 0.8), xycoords='axes fraction', fontsize=10)
        plt.legend()
        plt.grid(True)
        if filename is None:
            plt.show()
        else:
            plt.savefig(f'{filename}.png')

        




with open('analysis/data/strikerates.pickle', 'rb') as f:
    strikerates = pickle.load(f)
with open('analysis/data/mse.pickle', 'rb') as f:
    mse = pickle.load(f)
with open('analysis/data/data.pickle', 'rb') as f:
    df = pickle.load(f)
