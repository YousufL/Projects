from Clean import get_x_y
from Clean import MakeStats
from Clean import Clean
import scipy
import numpy 
import sklearn

#import sklearn.utils
from sklearn.linear_model import LogisticRegression

#from sklearn import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import preprocessing
from tqdm import tqdm
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
import numpy as np
RandomForest = RandomForestClassifier()
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

RandomForest = RandomForestClassifier()
Log = LogisticRegression(max_iter=1000)


df = pd.read_csv('Stats_Against (1).csv')

y = df.iloc[:,121]
X = df.iloc[:,120::]

print(y.head(5))


result = []
# Number of iterations
N_search = 20000
# Random seed initialization
np.random.seed(1)
for i in tqdm(range(N_search)):
    # Generate a random number of features
    N_columns =  list(np.random.choice(range(X.shape[1]),1)+1)

    # Given the number of features, generate features without replacement
    columns = list(np.random.choice(range(X.shape[1]), N_columns, replace=False))

    # Perform k-fold cross validation
    scores = cross_val_score(Log,X.iloc[:,columns], y, cv=5, scoring="accuracy")

    # Store the result
    result.append({'columns':columns,'performance':np.mean(scores),'Std': np.std(scores)})
    print(scores.mean())
# Sort the result array in descending order for performance measure
result.sort(key=lambda x : -x['performance'])
