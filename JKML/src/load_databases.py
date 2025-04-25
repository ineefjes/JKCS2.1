def load_databases(
    Qtrain,
    Qeval,
    Qopt,
    Qmonomers,
    Qhyper,
    method,
    VARS_PKL,
    TRAIN_HIGH,
    TRAIN_LOW,
    TEST_HIGH,
    TEST_LOW,
    MONOMERS_HIGH,
    MONOMERS_LOW,
):

    import os
    from pandas import read_pickle

    if Qtrain == 1 or Qhyper:
        if not os.path.exists(TRAIN_HIGH):
            print("Error reading file. TRAIN_HIGH = " + TRAIN_HIGH)
            exit()
        if method == "delta":
            if not os.path.exists(TRAIN_LOW):
                print("Error reading file. TRAIN_LOW = " + TRAIN_LOW)
                exit()
    if Qtrain == 2:
        if not os.path.exists(VARS_PKL):
            print("Error reading file. VARS_PKL = " + VARS_PKL)
            exit()
    if Qeval == 1 or Qeval == 2:
        if not os.path.exists(TEST_HIGH):
            print("Error reading file. + TEST_HIGH = " + TEST_HIGH)
            exit()
        if method == "delta":
            if not os.path.exists(TEST_LOW):
                if Qeval == 1:
                    TEST_LOW = TEST_HIGH
                else:
                    print("Error reading file. + TEST_LOW = " + TEST_LOW)
                    exit()
    if Qmonomers == 1:
        if not os.path.exists(MONOMERS_HIGH):
            print("Error reading file. MONOMERS_HIGH = " + MONOMERS_HIGH)
            exit()
        if method == "delta":
            if not os.path.exists(MONOMERS_LOW):
                print("Error reading file. MONOMERS_LOW = " + MONOMERS_LOW)
                exit()

    # IMPORTING THE REST OF LIBRARIES
    print("JKML is loading database(s).", flush=True)

    # LOADING THE DATABASES
    train_high_database = "none"
    train_low_database = "none"
    test_high_database = "none"
    test_low_database = "none"
    monomers_high_database = "none"
    monomers_low_database = "none"
    if Qtrain == 1 or Qhyper:
        train_high_database = read_pickle(TRAIN_HIGH).sort_values(
            [("info", "file_basename")]
        )
        if method == "delta":
            train_low_database = read_pickle(TRAIN_LOW).sort_values(
                [("info", "file_basename")]
            )
    if Qeval == 1 or Qeval == 2 or Qopt > 0:
        test_high_database = read_pickle(TEST_HIGH).sort_values(
            [("info", "file_basename")]
        )
        if method == "delta":
            test_low_database = read_pickle(TEST_LOW).sort_values(
                [("info", "file_basename")]
            )
    if Qmonomers == 1:
        monomers_high_database = read_pickle(MONOMERS_HIGH).sort_values(
            [("info", "file_basename")]
        )
        if method == "delta":
            monomers_low_database = read_pickle(MONOMERS_LOW).sort_values(
                [("info", "file_basename")]
            )

    return (
        train_high_database,
        train_low_database,
        test_high_database,
        test_low_database,
        monomers_high_database,
        monomers_low_database,
    )
