###############################################################################
###############################################################################
###############################################################################


def training(
    Qrepresentation,
    Qkernel,
    Qsplit,
    strs,
    Y_train,
    krr_cutoff,
    lambdas,
    sigmas,
    varsoutfile,
    Qsplit_i,
    Qsplit_j,
):

    ### IMPORTS ###
    # TODO: Do I really need pandas?
    from pandas import DataFrame

    if Qrepresentation == "fchl":
        from qmllib.representations import generate_fchl18 as generate_representation
    elif Qrepresentation == "mbdf":
        from MBDF import generate_mbdf as generate_representation
    else:
        print("JKML(QML): Unknown representation: " + Qrepresentation)
        exit()
    from qmllib.solvers import cho_solve

    if Qkernel == "Gaussian":
        from qmllib.representations.fchl import (
            get_local_symmetric_kernels as JKML_sym_kernel,
        )
        from qmllib.representations.fchl import get_local_kernels as JKML_kernel
    else:
        from qmllib.representations.fchl import (
            laplacian_kernel_symmetric as JKML_sym_kernel,
        )
        from qmllib.representations.fchl import laplacian_kernel as JKML_kernel
    import numpy as np
    import pickle
    import time

    ### REPRESENTATION CALCULATION ###
    repr_wall_start = time.perf_counter()
    repr_cpu_start = time.process_time()
    if Qrepresentation == "fchl":
        repres_dataframe = DataFrame(index=strs.index, columns=["xyz"])
        max_atoms = max(
            [len(strs.iloc[i].get_atomic_numbers()) for i in range(len(strs))]
        )
        for i in range(len(repres_dataframe)):
            # repres_dataframe["xyz"].iloc[i] = generate_representation(strs.iloc[i].get_positions(), strs.iloc[i].get_atomic_numbers(),max_size = max_atoms, neighbors = max_atoms, cut_distance=krr_cutoff)
            repres_dataframe["xyz"].iloc[i] = generate_representation(
                strs.iloc[i].get_atomic_numbers(),
                strs.iloc[i].get_positions(),
                max_size=max_atoms,
                neighbors=max_atoms,
                cut_distance=krr_cutoff,
            )
        X_atoms = None
        X_train = np.array([mol for mol in repres_dataframe["xyz"]])
    elif Qrepresentation == "mbdf":
        X_atoms = [strs[i].get_atomic_numbers() for i in range(len(strs))]
        X_train = generate_representation(
            np.array([i.get_atomic_numbers() for i in strs]),
            np.array([i.get_positions() for i in strs]),
            cutoff_r=krr_cutoff,
            normalized=False,
        )

    repr_train_wall = time.perf_counter() - repr_wall_start
    repr_train_cpu = time.process_time() - repr_cpu_start
    # some info about the full representation
    print(
        "JKML(QML): Shape of the training representation: " + str(X_train.shape),
        flush=True,
    )

    train_wall_start = time.perf_counter()
    train_cpu_start = time.process_time()
    # ONLY FOR JOINING ALL THE SPLITS AND CHOLESKY DECOMPOSITION
    if Qsplit == -1:
        splits = Qsplit_i + 1
        K = []
        for i in range(0, splits):
            Kx = []
            for j in range(0, splits):
                if i < j:
                    s1 = j
                    s2 = i
                else:
                    s1 = i
                    s2 = j
                f = open(
                    varsoutfile.split(".pkl")[0]
                    + "_"
                    + str(splits)
                    + "_"
                    + str(s1)
                    + "_"
                    + str(s2)
                    + ".pkl",
                    "rb",
                )
                Kcell, Y_train = pickle.load(f)
                if i > j:
                    Kcell = np.transpose(Kcell[0])
                else:
                    Kcell = Kcell[0]
                if len(Kx) == 0:
                    Kx = Kcell
                else:
                    Kx = np.concatenate((Kx, Kcell))
                f.close()
            if len(K) == 0:
                K = Kx
            else:
                K = np.concatenate((K, Kx), axis=1)
        alpha = [cho_solve(K, Y_train)]
        train_wall = time.perf_counter() - train_wall_start
        train_cpu = time.perf_counter() - train_cpu_start
        f = open(varsoutfile, "wb")
        pickle.dump([X_train, sigmas, alpha], f)
        f.close()
        print("JKML(QML): Training completed.", flush=True)
    elif Qsplit == 1:
        if Qrepresentation == "fchl":
            K = JKML_sym_kernel(
                X_train, kernel_args={"sigma": sigmas}
            )  # calculates kernel
        elif Qrepresentation == "mbdf":
            K = [JKML_sym_kernel(X_train, X_atoms, sigmas[0])]  # calculates kernel
        K = [
            K[i] + lambdas[i] * np.eye(len(K[i])) for i in range(len(sigmas))
        ]  # corrects kernel
        alpha = [
            cho_solve(Ki, Y_train) for Ki in K
        ]  # calculates regression coeffitients
        train_wall = time.perf_counter() - train_wall_start
        train_cpu = time.process_time() - train_cpu_start

        # I will for now everytime save the trained QML
        f = open(varsoutfile, "wb")
        if Qrepresentation == "fchl":
            pickle.dump([X_train, sigmas, alpha], f)
        elif Qrepresentation == "mbdf":
            pickle.dump([X_train, X_atoms, sigmas, alpha], f)
        f.close()
        print("JKML(QML): Training completed.", flush=True)
    else:
        X_train_i = np.array_split(X_train, Qsplit)[Qsplit_i]
        X_train_j = np.array_split(X_train, Qsplit)[Qsplit_j]
        if Qsplit_i == Qsplit_j:
            K = JKML_sym_kernel(
                X_train_i, kernel_args={"sigma": sigmas}
            )  # calculates kernel
            K = [
                K[i] + lambdas[i] * np.eye(len(K[i])) for i in range(len(sigmas))
            ]  # corrects kernel
        else:
            K = JKML_kernel(X_train_i, X_train_j, kernel_args={"sigma": sigmas})
        train_wall = time.perf_counter() - train_wall_start
        train_cpu = time.process_time() - train_cpu_start
        f = open(
            varsoutfile.split(".pkl")[0]
            + "_"
            + str(Qsplit)
            + "_"
            + str(Qsplit_i)
            + "_"
            + str(Qsplit_j)
            + ".pkl",
            "wb",
        )
        pickle.dump([K, Y_train], f)
        f.close()
        alpha = None
        print("JKML(QML): Training completed.", flush=True)
    n_train = X_train.shape[0]
    d_train = np.sum(X_train.shape[1:])

    return {
        key: value
        for key, value in locals().items()
        if key
        in [
            "X_train",
            "X_atoms",
            "alpha",
            "repr_train_wall",
            "repr_train_cpu",
            "train_wall",
            "train_cpu",
            "n_train",
            "d_train",
        ]
    }


###############################################################################
###############################################################################
###############################################################################


def evaluate(Qrepresentation, krr_cutoff, X_train, sigmas, alpha, strs, Qkernel):

    from pandas import DataFrame
    import time

    if Qrepresentation == "fchl":
        from qmllib.representations import generate_fchl18 as generate_representation
    elif Qrepresentation == "mbdf":
        from MBDF import generate_mbdf as generate_representation
    else:
        print("JKML(QML): Unknown representation: " + Qrepresentation)
        exit()
    from qmllib.solvers import cho_solve

    if Qkernel == "Gaussian":
        from qmllib.representations.fchl import get_local_kernels as JKML_kernel
    else:
        from qmllib.representations.fchl import laplacian_kernel as JKML_kernel
    import numpy as np

    repr_wall_start = time.perf_counter()
    repr_cpu_start = time.process_time()
    ### REPRESENTATION CALCULATION ###
    if Qrepresentation == "fchl":
        repres_dataframe = DataFrame(index=strs.index, columns=["xyz"])
        max_atoms = max(
            [len(strs.iloc[i].get_atomic_numbers()) for i in range(len(strs))]
        )
        for i in range(len(repres_dataframe)):
            # repres_dataframe["xyz"][i] = generate_representation(strs[i].get_positions(), strs[i].get_atomic_numbers(),max_size = max_atoms, neighbors = max_atoms, cut_distance=krr_cutoff)
            repres_dataframe["xyz"].iloc[i] = generate_representation(
                strs.iloc[i].get_atomic_numbers(),
                strs.iloc[i].get_positions(),
                max_size=max_atoms,
                neighbors=max_atoms,
                cut_distance=krr_cutoff,
            )
        X_test = np.array([mol for mol in repres_dataframe["xyz"]])
    elif Qrepresentation == "mbdf":
        X_test_atoms = [strs[i].get_atomic_numbers() for i in range(len(strs))]
        X_test = generate_representation(
            np.array([i.get_atomic_numbers() for i in strs]),
            np.array([i.get_positions() for i in strs]),
            cutoff_r=krr_cutoff,
            normalized=False,
        )

    repr_test_wall = time.perf_counter() - repr_wall_start
    repr_test_cpu = time.process_time() - repr_cpu_start
    # some info about the full representation
    print(
        "JKML(QML): Shape of the testing representation: " + str(X_test.shape),
        flush=True,
    )

    ### CORRECTING THE FCHL MATRIX SIZES
    # IF YOU ARE EXTENDING THIS WILL MAKE THE MATRIXES OF THE SAME SIZE
    if Qrepresentation == "fchl":
        if X_train.shape[1] != X_test.shape[1]:
            if X_train.shape[1] > X_test.shape[1]:
                small = X_test
                large = X_train
            else:
                small = X_train
                large = X_test
            newmatrix = np.zeros([small.shape[0], large.shape[1], 5, large.shape[3]])
            newmatrix[:, :, 0, :] = 1e100
            newmatrix[
                0 : small.shape[0], 0 : small.shape[1], 0:5, 0 : small.shape[3]
            ] = small
            if X_train.shape[1] > X_test.shape[1]:
                X_test = newmatrix
            else:
                X_train = newmatrix

    test_wall_start = time.perf_counter()
    test_cpu_start = time.process_time()
    ### THE EVALUATION
    if Qrepresentation == "fchl":
        Ks = JKML_kernel(X_test, X_train, kernel_args={"sigma": sigmas})
    elif Qrepresentation == "mbdf":
        Ks = [JKML_kernel(X_train, X_test, X_atoms, X_test_atoms, sigmas[0])]
    Y_predicted = [np.dot(Ks[i], alpha[i]) for i in range(len(sigmas))]

    test_wall = time.perf_counter() - test_wall_start
    test_cpu = time.process_time() - test_cpu_start
    d_test = np.sum(X_test.shape[1:])
    return Y_predicted, repr_test_wall, repr_test_cpu, test_wall, test_cpu, d_test


###############################################################################
###############################################################################
###############################################################################


def optimize(
    strs,
    Qrepresentation,
    krr_cutoff,
    varsoutfile,
    Qsplit,
    nn_cutoff,
    Qkernel,
    Qopt,
    opt_maxstep,
    opt_dump,
    opt_steps,
    md_temperature,
    md_thermostatfriction,
    md_dump,
    md_steps,
):

    # IMPORTS
    import numpy as np

    if Qrepresentation == "fchl":
        from qmllib.representations import generate_fchl18 as generate_representation
    elif Qrepresentation == "mbdf":
        from MBDF import generate_mbdf as generate_representation
    else:
        print("JKML(QML): Unknown representation: " + Qrepresentation)
        exit()
    from qmllib.solvers import cho_solve

    if Qkernel == "Gaussian":
        from qmllib.representations.fchl import get_local_kernels as JKML_kernel
    else:
        from qmllib.representations.fchl import laplacian_kernel as JKML_kernel

    print("JKML(QML): Preparing optimization", flush=True)
    print(
        "JKML(QML): WARNING: These are just some shit numerical calculations",
        flush=True,
    )
    print("JKML(QML): WARNING", flush=True)
    print("JKML(QML): WARNING", flush=True)
    print("JKML(QML): WARNING", flush=True)
    print("JKML(QML): WARNING", flush=True)
    print("JKML(QML): WARNING", flush=True)
    print("JKML(QML): WARNING", flush=True)
    print("JKML(QML): WARNING", flush=True)
    print("JKML(QML): WARNING", flush=True)
    print("JKML(QML): WARNING", flush=True)
    xyz = strs[0].get_positions()
    # F=np.zeros_like(xyz)
    # for i in range(len(xyz)):
    #      for j in range(3):
    #            F[i,j]=float(13.0)
    # print(F[0,0], flush = True)
    # print(xyz[0,0]+0.23, flush = True)
    # print(type(xyz), flush = True)
    maxsteps = 8
    xyzdeviation = 0.05
    shift = 0.3
    print("JKML(QML): Starting optimization", flush=True)
    for step in range(maxsteps):
        ### GENERATE SHIFTED STRUCTURES

        R = [xyz]
        if step != maxsteps - 1:
            for i in range(len(xyz)):
                for j in range(3):
                    ch = np.zeros_like(xyz)
                    ch[i, j] = +xyzdeviation  # THIS IS THE SHIFT OF 0.05 Angstrom
                    R.append(xyz + ch)
                    # ch=-ch
                    # R.append(xyz+ch)

        RR = pd.DataFrame(np.zeros(len(R)), index=range(len(R)))
        RR[0] = R
        # print(RR, flush = True)

        if method == "delta":
            for RR_iter in range(len(RR[0])):
                # print(RR_iter,flush = True)
                os.system("mkdir test;")
                tocalc = strs[0].copy()
                tocalc.set_positions(RR[0][RR_iter])
                write("test/test.xyz", tocalc)
                os.system(
                    "cd test;xtb test.xyz --sp --gfn 1 > test.log 2>&1 ;cd ..;JKQC -folder test -out JKMLtest.pkl -noex;rm -r test"
                )
                os.system("JKQC JKMLtest.pkl -el > .en")
                with open(".en", "r") as ping:
                    en = float(ping.read().rstrip())
                # print(en, flush=True)
                if RR_iter == 0:
                    all_ens = [en]
                else:
                    all_ens.append(en)
                # print(all_ens, flush = True)
            # print(all_ens, flush = True)

        # print(RR.values[0][0], flush = True)
        ### REPRESENTATION CALCULATION ###
        repres_dataframe = pd.DataFrame(index=RR.index, columns=["xyz"])
        max_atoms = max([len(strs[i].get_atomic_numbers()) for i in range(len(strs))])
        for i in range(
            len(repres_dataframe)
        ):  # TODO strs[0] cannot be define like that for different molecules, i.e. I can optimize only 1 molecule
            repres_dataframe["xyz"][i] = generate_representation(
                RR.values[i][0],
                strs[0].get_atomic_numbers(),
                max_size=max_atoms,
                neighbors=max_atoms,
                cut_distance=krr_cutoff,
            )
        fchl_representations = np.array([mol for mol in repres_dataframe["xyz"]])

        # some info about the full representation
        # print(fchl_representations.shape, flush = True)

        ### DEFINING THE EVALUATION Xs:  Y = QML(X)
        # the full set
        X_test = fchl_representations

        ### CORRECTING THE FCHL MATRIX SIZES
        # X_train = fchl_representations0
        # IF YOU ARE EXTENDING THIS WILL MAKE THE MATRIXES OF THE SAME SIZE
        if X_train.shape[1] != X_test.shape[1]:
            if X_train.shape[1] > X_test.shape[1]:
                small = X_test
                large = X_train
            else:
                small = X_train
                large = X_test
            newmatrix = np.zeros([small.shape[0], large.shape[1], 5, large.shape[3]])
            newmatrix[:, :, 0, :] = 1e100
            newmatrix[
                0 : small.shape[0], 0 : small.shape[1], 0:5, 0 : small.shape[3]
            ] = small
            if X_train.shape[1] > X_test.shape[1]:
                X_test = newmatrix
            else:
                X_train = newmatrix

        ### THE EVALUATION
        Ks = JKML_kernel(X_test, X_train, kernel_args={"sigma": sigmas})
        Y_predicted = [np.dot(Ks[i], alpha[i]) for i in range(len(sigmas))]

        if method == "delta":
            new_save_energy = Y_predicted[0][0] + all_ens[0]
        else:
            new_save_energy = Y_predicted[0][0]
        if step != 0:
            if new_save_energy > save_energy:
                xyz = xyz + change
                shift = shift / 2
                continue

        xyzold = xyz
        F = np.zeros_like(xyz)
        if step != maxsteps - 1:
            Fp = np.zeros_like(xyz)
            # Fm=np.zeros_like(xyz)
            for i in range(len(xyz)):
                for j in range(3):
                    if method == "delta":
                        # print(Y_predicted[0][0])
                        # print(all_ens[0])
                        # print(wtf1)
                        # print(F[i,j])
                        F[i, j] = Y_predicted[0][0] + all_ens[0]
                        # print(F[i,j])
                        Fp[i, j] = (
                            Y_predicted[0][1 + j + 3 * i] + all_ens[1 + j + 3 * i]
                        )
                    else:
                        F[i, j] = Y_predicted[0][0]
                        Fp[i, j] = Y_predicted[0][1 + j + 3 * i]
                    # Fp[i,j]=Y_predicted[0][1+2*j+6*i]
                    # Fm[i,j]=Y_predicted[0][2+2*j+6*i]

            # print(np.linalg.inv((Fm+Fp-2*F)/(2*xyzdeviation)))
            # print(xyz+0.5*np.matmul(np.linalg.inv((Fm+Fp-2*F)/(2*xyzdeviation)),(Fp-Fm)/(2*xyzdeviation)), flush = True)
            change = (Fp - F) / xyzdeviation * shift
            xyz = xyz - change
            # print("TEST:",flush = True)
            # print(change, flush = True)
            # print(change*change, flush = True)
            # print(np.transpose(change*change),flush=True)
            # print(sum(np.transpose(change*change)),flush=True)
            # print(np.sqrt(sum(np.transpose(change*change))),flush = True)
            maxdev = max(np.sqrt(sum(np.transpose(change * change))))

        if step == 0:
            print("JKML(QML): step \tenergy [Eh]        \tmax.shift [A]", flush=True)
            clustersout_df = pd.DataFrame()
        save_energy = new_save_energy
        cluster_id = len(clustersout_df)
        clustersout_df = df_add_append(
            clustersout_df,
            "info",
            "folder_path",
            [str(cluster_id)],
            os.path.abspath(TEST_HIGH)[::-1].split("/", 1)[1][::-1] + "/",
        )
        clustersout_df = df_add_iter(
            clustersout_df,
            column_name_1,
            column_name_2,
            [str(cluster_id)],
            [save_energy],
        )
        newxyz = strs[0].copy()
        newxyz.set_positions(xyzold)
        clustersout_df = clustersout_df = df_add_iter(
            clustersout_df, "xyz", "structure", [str(cluster_id)], [newxyz]
        )
        print(
            "JKML(QML): " + str(step) + " \t" + str(save_energy) + " \t" + str(maxdev),
            flush=True,
        )
        # print(xyz, flush = True)
