import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from transfers.fileio import dump_to_pickle, load_from_pickle
from helpers.preprocessing import process_features, process_payment
from model.model import StatusModel
from model.validate import actual_IRR


def test_expected_current():
    print "Loading data..."
    df_3c = pd.read_csv('data/LoanStats3c_securev1.csv', header=True).iloc[:-2, :]
    df_3b = pd.read_csv('data/LoanStats3b_securev1.csv', header=True).iloc[:-2, :]
    df_raw = pd.concat((df_3c, df_3b), axis=0)
    
    print "Pre-processing data..."
    df = process_features(df_raw)

    print "Initializing model..."
    model = StatusModel(model=RandomForestRegressor,
                        parameters={'n_estimators':100,
                                     'max_depth':10})

    print "Training model..."
    model.train_statusmodel(df)
    # dump_to_pickle(model, 'pickle/model_test.pkl')
    model = load_from_pickle('pickle/model_test.pkl')

    print "Calculating IRR..."
    int_rate_dict = {'A1':0.0603, 'A2':0.0649, 'A3':0.0699, 'A4':0.0749, 'A5':0.0819,
                     'B1':0.0867, 'B2':0.0949, 'B3':0.1049, 'B4':0.1144, 'B5':0.1199,
                     'C1':0.1239, 'C2':0.1299, 'C3':0.1366, 'C4':0.1431, 'C5':0.1499,
                     'D1':0.1559, 'D2':0.1599, 'D3':0.1649, 'D4':0.1714, 'D5':0.1786}

    IRR = model.expected_IRR(df.iloc[:10, :], True)
    print "Expected IRR calculated with default int_rate:", IRR
    
    IRR = model.expected_IRR(df.iloc[:10, :], False, int_rate_dict)
    print "Expected IRR calculated with custom int_rate:", IRR

    IRR = model.expected_IRR(df.iloc[:10, :], True, {}, False, 0.01)
    print "Expected IRR calculated with custom compounding curve:", IRR


def test_actual_matured():
    print "Loading data..."
    df_3a = pd.read_csv('data/LoanStats3a_securev1.csv', header=True).iloc[:-2, :]
    df_raw = df_3a.copy()

    print "Pre-processing data..."
    df = process_payment(df_raw)

    print "Calculating IRR..."
    int_rate_dict = {'A1':0.0603, 'A2':0.0649, 'A3':0.0699, 'A4':0.0749, 'A5':0.0819,
                     'B1':0.0867, 'B2':0.0949, 'B3':0.1049, 'B4':0.1144, 'B5':0.1199,
                     'C1':0.1239, 'C2':0.1299, 'C3':0.1366, 'C4':0.1431, 'C5':0.1499,
                     'D1':0.1559, 'D2':0.1599, 'D3':0.1649, 'D4':0.1714, 'D5':0.1786}
    
    IRR = actual_IRR(df.iloc[:10, :], True)
    print "Actual IRR calculated with default int_rate:", IRR

    IRR = actual_IRR(df.iloc[:10, :], False, int_rate_dict)
    print "Actual IRR calculated with custom int_rate:",  IRR

    IRR = actual_IRR(df.iloc[:10, :], True, {}, False, 0.01)
    print "Actual IRR calculated with custom compounding curve:", IRR


if __name__ == '__main__':
    test_expected_current()
    test_actual_matured()