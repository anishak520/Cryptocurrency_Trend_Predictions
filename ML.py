# Import the required libraries and dependencies
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings

# Disable warnings
warnings.simplefilter(action='ignore')

def get_num_cols(df):
    """Extract numerical columns from the DataFrame."""
    return [col for col in df.columns if df[col].dtype in ['float64', 'int64']]

def get_scaled(df, num_cols, dummies_cols=None):
    """Scale numerical columns and concatenate dummy variables if specified."""
    # Scale numerical columns
    scaled_df = pd.DataFrame(StandardScaler().fit_transform(df[num_cols]), columns=num_cols)
    
    # Encode dummy variables if specified
    if dummies_cols:
        dummies_df = pd.get_dummies(df[dummies_cols], drop_first=True)
        scaled_df = pd.concat([scaled_df, dummies_df], axis=1)
    
    return scaled_df

def get_elbow(df):
    """Compute inertia for a range of k values to determine the elbow point."""
    inertia = []
    k_range = range(1, 11)

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=1)
        model.fit(df)
        inertia.append(model.inertia_)
    
    return pd.DataFrame({'k': list(k_range), 'inertia': inertia})

def fit_model(df, clusters):
    """Fit KMeans model and assign cluster labels."""
    model = KMeans(n_clusters=clusters, random_state=1)
    df['cluster'] = model.fit_predict(df)
    return df
