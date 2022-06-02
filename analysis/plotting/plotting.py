from matplotlib import pyplot as plt
import pickle


def plot(strikerates, mse, title=None):
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
        for value in strikerates.values():
            if value['mean_prediction'] is not None:
                mean_predictions.append(value['mean_prediction'])
            if value['strikerate'] is not None:
                strikerates_list.append(value['strikerate'])

        plt.plot(mean_predictions, strikerates_list, color='green', linestyle='-', marker='.')
        plt.xlabel('Mean Predictions')
        plt.ylabel('Strikerate')
        plt.annotate('MSE: ' + str(mse), xy=(0.8, 0.05), xycoords='axes fraction', fontsize=12)
        plt.grid(True)
        
        plt.show()



with open('analysis/data/strikerates.pickle', 'rb') as f:
    strikerates = pickle.load(f)
with open('analysis/data/mse.pickle', 'rb') as f:
    mse = pickle.load(f)
plot(strikerates, mse, title='Strikerate vs Mean Prediction')
