####################################################################################################

def print_help():
  print("##################################################")
  print("### python JKQC.py [FILES] [ARGUMENTS] [PRINT] ###")
  print("\nFILES:")
  print(" any .xyz .log .out files")
  print(" any .pkl (you can also use -in/-out)")
  print("\nARGUMENTS:")
  print(" -help       print this help")
  print(" -info       information about a database")
  print(" -in X.pkl   read data from a database")
  print(" -out X.pkl  save data to XX.pkl (-noex = do not print example)")
  print(" -orcaext X  if ORCA has different extension than out")
  print(" -folder X   takes in all X/*.log files (use -R for resursive)")
  print(" -noname     the file names are not analysed (e.g. 1000-10_1.xyz)")
  print(" -rename X Y renames e.g. 1X2sa to 1Y2sa")
  print(" -extract X  prints only selected clusters (e.g. 1sa1w,1sa3-4w or 1sa1w-1_0)")
  print(" -except X   prints only non-selected clusters (e.g. 1sa1w,1sa3-4w or 1sa1w-1_0)")
  print(" -reacted    removes (the minority of) reacted structures")
  print(" -noexample,-noex does not print an example")
  print("\nPRINT:")
  print(" -ct                cluster type (e.g. 1sa,3sa2am)")
  print(" -b                 basename (e.g. 1sa-3, 3sa2am-4_508)")
  print(" -nXYZ,-nLOG,-nOUT  name with its extension")
  print(" -pXYZ,-pLOG,-pOUT  full_path/name with its extension")
  print(" -ePKL              pkl_full_filepath/:EXTRACT:/basename")
  print(" -el       electronic energy from .log [Eh]   -elSP        single-point el.en. (1. in .log) [Eh]")
  print(" -elout    el. energy from .out [Eh]          -rot         RMSD of rotational constants [GHz]") 
  print(" -elc      elc=elout-el [Eh]                  -rots        rotational constants [GHz]")
  print(" -zpec     ZPE correction [Eh]                -mult        muliplicity [-]")
  print(" -zpe      ZPE=el+zpec [Eh]                   -char,-chrg  charge [-electron_charge]")
  print(" -zpeout   ZPEout=elout+zpec [Eh]             -dip         dipole moment [Debye]")
  print(" -uc       energy thermal correction [Eh]     -dips        dipole moments [Debye]")
  print(" -u        internal energy U=el+uc [Eh]       -pol         polarizability [Angstrom^3]")
  print(" -uout     Uout=elout+uc [Eh]                 -templog     temperature used in .log [K]")
  print(" -hc       enthalpy th. corr. hc=uc+kT [Eh]   -preslog     pressure used in .log [atm]")
  print(" -h        enthalpy energy H=el+hc [Eh]       -lf          the lowest vib. freq. [1/cm]")
  print(" -hout     Hout=elout+hc [Eh]                 -f           array of vibration freq. [1/cm]")
  print(" -s        entropy [Eh/K]                     -rsn         rotational symmetry number [-]")
  print(" -gc       Gibbs free energy th. corr. [Eh]   -t,-time     total computational (elapsed) time [mins]")
  print(" -g        Gibbs free energy [Eh]             -termination count lines with \"Normal termination\" status")
  print(" -gout     G with el.en.corr.:Gout=G+elc [Eh] -mi          moments of inertia")
  print(" -mull     Mulliken charges [-el.charge]      -ami         average moment of inertia")
  print(" -xyz      save all XYZ files                 -rg          radius of gyration [Angstrom]")
  print(" -movie    save all XYZs to movie.xyz         -radius      approx. radius of cluster size [Angstrom]")
  print(" -charges  save all Mulliken .charges files   -radius0.5   radius with +0.5 Angstrom correction")
  print(" -mass     prints molecular mass [g/mol]      -level       program version and method used")
  print("\nPOST-CALCULATIONS:")
  print(" -fc [value in cm^-1] frequency cut-off for low-vibrational frequencies CITE: Grimme")
  print(" -temp [value in K]   recalculate for different temperature")
  print(" -v,-as [value]       anharmonicity scaling factor CITE: Grimme")
  print(" -unit                converts units [Eh] -> [kcal/mol] (for entropy: [Eh/K] -> [cal/mol/K])")
  print("\nFILTERING:")
  print(" -sort <str>          sort by: g,gout,el,elout,<full name in database under log>")
  print(" -select <int>        selects <int> best structures from each cluster")
  print(" -uniq,-unique <str>  selects only unique based on, e.g.: rg,el or rg,g or rg,el,dip, or dup=duplicates")
  print(" -sample <int> <str>  selects <INT> distinct based on, e.g.: rg,el or rg,g or rg,el,dip")
  print("                      use e.g. rg2,el0.5 to define threshold as 10**-x [def: rg=2, el/g=3, dip=1]")
  print(" -arbalign <float>    use (modified) ArbAlign program to compare RMSD (by def sort -el). CITE ArbAlign!!")
  print(" -cut/-pass X Y       removes higher/lower values of X=rg,el,g... with cutoff Y (e.g. -cut el -103.45)")
  print(" -cutr/-passr X Y     removes higher/lower rel. values compared to lowest of X=rg,el,g... with cutoff Y (e.g. -cutr g 5)")
  print("   OR")
  print(" -filter_lt/le/==/ge/gt/ne  X Y      filter absolute value of X compared to Y value (e.g. -filter_le rg 3.0)")
  print(" -rel_filter_lt/le/==/ge/gt/ne  X Y  filter minimum-relative value of X compared to Y value (e.g. -rel_filter_lt el 5.0)")
  print("                                     lt=less than/le=less or equal/ge=greater or equal/gt=greater than/ne=not equal")
  print(" -filter_== bonded <float thr.> <element> <element> <Y>  example of filtering for number of bond distances")
  print("\nFORMATION PROPERTIES:")
  print(" -pop                    prints column of population probability")
  print(" -glob OR -globout       prints only values for clusters with the lowest -g OR -gout")
  print(" -bavg OR -bavgout       prints a value that is Boltzmann average over each cluster using -g OR -gout")
  print("                         NOTE: -g/-gout is treated correctly + -s not treated; use (G - H)/T")
  print(" -formation              print values as formation ")
  print(" <input_file> -formation print formations for the input file (no averaging though)")
  print(" -conc sa 0.00001        dG at given conc. [conc in Pa] (or use ppt,ppb,cmmc. e.g. 100ppt")
  print("                         use -cnt for self-consistent dG")
  print("\nOTHERS:")
  print(" -add <column> <file>, -extra <column>, -rebasename, -presplit, -i/-index <int:int>, -imos, -imos_xlsx,")
  print(" -forces [Eh/Ang], -shuffle, -split <int>, -underscore, -addSP <pickle>, -complement <pickle>")
  print(" -column <COL1> <COL2>, -drop <COL>, -out2log, -levels, -atoms, -natoms, -hydration/-solvation <str>")
  print(" -rh <0.0-1.0>, -psolvent <float in Pa>, -anharm, -test, -bonded <float thr.> <element> <element>")

#OTHERS: -imos,-imos_xlsx,-esp,-chargesESP

def arguments(argument_list = []):
  from os import path
  missing = float("nan")
  
  #global folder,Qcollect,Qrecursive,files,input_pkl,input_pkl_sp,output_pkl,Qforces
  folder = "./"	
  Qcollect = "log" #what extension am I collecting?
  Qrecursive = False
  files = []  
  input_pkl = []
  input_pkl_sp = []
  output_pkl = "mydatabase.pkl"
  Qforces = 0 #should I collect forces? 0/1
  
  #global addcolumn,Qmodify,Qrename,QrenameWHAT,Qiamifo,Qrebasename,Qunderscore,Qchangeall,Qcomplement,QcolumnDO,Qcolumn
  addcolumn = []
  Qmodify = 0 #Do I want to somehow modify the input dataframe or names?
  Qrename = 0 #Do I want to rename some monomer? 
  QrenameWHAT = [] #Do I want to rename some monomer? 
  Qiamifo = 0 #This is calling renaming only for Ivo Neefjes
  Qrebasename = 0 #change names if they are the same 
  Qunderscore = 0 #underscore to dash
  Qchangeall = 0 #do I want to some column to all
  Qcomplement = 0 #subtract these from the list base on basename of the new pickle file
  QcolumnDO = 0
  Qcolumn = []
 
  #global Qclustername,Qextract,Pextract,Qreacted,bonddistancethreshold 
  Qclustername = 1 #Analyse file names for cluster definition?
  Qextract = 0 #Do I want to extarct only some cluster_type(s)?
  Pextract = []
  Qreacted = 0 #Remove reacted structures?, 1 = yes; 2 = print the reverse 
  bonddistancethreshold = 1.75
  Qbonded = []
  
  #global Qoutpkl,Qout,Pout,QUenergy,QUentropy
  Qoutpkl = 0 #Do I want to save output.pkl? 0=NO,1=YES
  Qout = 1 #output level. 0=only neccessary,1=yes,2=rich print
  Pout = []
  QUenergy = 1 #if you want to energy 
  QUentropy = 1 #if you want to energy 
  
  #global Qqha,Qt,Qp,Qfc,Qanh,Qanharm
  Qqha = 0 #Run the QHA
  Qt = missing
  Qp = missing
  Qfc = 0 #Run QHA with vib. frequency cutoff
  Qanh = 1
  Qanharm = 0 #To collect anharmonicities from QC output
 
  #global Qpresplit,Qsplit,Qindex,Qdrop,Qout2log 
  Qpresplit = 0 #Do I want to take only part of the data?
  Qsplit = 1 #should I split the base on several parts
  Qindex = "-1"#
  Qdrop = "0" #drop some column
  Qout2log = 0 #change column name
  
  #global Qsort,Qselect,Qsample,Quniq,Qarbalign,formation_input_file,Qthreshold,Qcut,Qshuffle
  Qsort = 0 # 0=no sorting, otherwise string
  Qselect = 0 # 0=nothing, otherwise the number of selected structures
  Qsample = 0 # The same as uniqueness but adjustable automatically
  Quniq = 0 # uniqie based on given arguments
  Qarbalign = 0 #use ArbAlign with float parameter
  formation_input_file = ""
  Qthreshold = 0 #cut/pass something
  Qcut = [] #what will be cutted
  Qshuffle = 0 #shuffle rows
  
  #global Qglob,Qbavg,Qrh,QPsolvent,Qformation,Qconc,conc,CNTfactor,Qsolvation
  Qglob = 0 # 1=values for lowest -g, 2=values for lowest -gout
  Qbavg = 0 # 1=Boltzmann avg over -g, 2=Boltzmann avg over -gout
  Qrh = missing
  QPsolvent = missing
  Qformation = 0
  Qconc = 0
  conc = []
  CNTfactor = 0 #see Wyslouzil
  Qsolvation = "0"
  
  #global folderMAIN,folderSP
  folderMAIN = ""
  folderSP = ""
  
  #global orcaext,orcaextname,mrccextname,turbomoleext,turbomoleextname
  orcaext = "out"
  orcaextname = "out"
  mrccextname = "out"
  turbomoleext = "out"
  turbomoleextname = "out"
 
  last = ""
  for i in argument_list:
    #HELP
    if i == "-help" or i == "--help":
      print_help()
      exit()
    #FOLDER
    if i == "-folder":
      last = "-folder"
      continue
    if last == "-folder":
      last = ""
      if path.exists(i):
        folder = i
        continue
      else:
        print("Folder "+i+" does not exist. [EXITING]")
        exit()
    #COLLECT
    if i == "-collect" or i == "-col" or i == "-coll":
      last = "-collect"
      continue
    if last == "-collect":
      last = ""
      Qcollect = str(i)
      continue
    if i == "-R":
      Qrecursive = True
      continue
    #INPKL
    if i == "-in":
      last = "-in"
      continue
    if last == "-in":
      last = ""
      if path.exists(i):    
        input_pkl.append(i)
        continue
      else:
        print("File "+i+" does not exist. Sorry [EXITING]")
        exit()
    #INPKL SP
    if i == "-addSP":
      last = "-addSP"
      continue
    if last == "-addSP":
      last = ""
      if path.exists(i):
        input_pkl_sp.append(i)
        continue
      else:
        print("File "+i+" does not exist. Sorry [EXITING]")
        exit()
    #OUTPKL
    if i == "-out" or i == "-o":
      last = "-out"
      continue
    if last == "-out":
      last = ""
      if output_pkl != "mydatabase.pkl":
        print("Hey are you trying to use two different outputs? "+output_pkl+"/"+i+" [EXITING]")
        exit()
      else:
        output_pkl = i
        if Qoutpkl == 0:
          Qoutpkl = 1
        continue
    #Hydration
    if i == "-hydration":
      Qsolvation = "w"
      continue
    #Anharm
    if i == "-anharm":
      Qanharm = 1
      continue
    #Qrh
    if i == "-rh":
      last = "-rh"
      continue
    if last == "-rh":
      last = ""
      Qrh = float(i)
      continue
    #psolvent
    if i == "-psolvent":
      last = "-psolvent"
      continue
    if last == "-psolvent":
      last = ""
      QPsolvent = float(i)
      continue
    #Solvation
    if i == "-solvation":
      last = "-solvation"
      continue
    if last == "-solvation":
      last = ""
      Qsolvation = str(i)
      continue
    #bonded
    if i == "-bonded":
      last = "-bonded"
      rem = []
      continue
    if last == "-bonded":
      last = "-bonded1"
      rem.append(str(i))
      continue
    if last == "-bonded1":
      last = "-bonded2"
      rem.append(str(i))
      continue
    if last == "-bonded2":
      last = ""
      rem.append(str(i))
      Qbonded.append(rem)
      rem = ""
      Pout.append("-bonded")
      continue
    #IamIfo
    if i == "-IamIfo":
      Qmodify = 1
      Qiamifo = 1
      continue
    #FORCES
    if i == "-forces":
      Qforces = 1
      continue
    #ORCA EXTENSION
    if i == "-orcaext" or i == "-orca":
      last = "-orcaext"
      continue
    if last == "-orcaext":
      last = ""
      orcaext = str(i)
      orcaextname = "log"
      continue
    #TURBOMOLE EXTENSION
    if i == "-turbomoleext" or i == "-turbomole":
      last = "-turbomoleext"
      continue
    if last == "-turbomoleext":
      last = ""
      turbomoleext = str(i)
      turbomoleextname = "log"
      continue
    #COLUMN 
    if i == "-column":
      last = "-column"
      QcolumnDO += 1
      Pout.append("-column")
      continue
    if last == "-column":
      last = "-column1"
      QcolumnADD = str(i)
      continue
    if last == "-column1":
      last = ""
      Qcolumn.append([QcolumnADD, str(i)])
      continue
    #LEVELS
    if i == "-levels":
      Pout.append("-levels")
      continue
    #ADD EXTRA COLUMN
    if i == "-add" or i == "-addcolumn":
      last = "-add"
      continue
    if last == "-add":
      last = "-add2"
      columnname = str(i)
      continue
    if last == "-add2":
      last = "" 
      if path.exists(str(i)):
        addcolumn.append([columnname, str(i)])
        continue
      else:
        print("File "+i+" does not exist. Sorry [EXITING]")
        exit()       
    #NONAME
    if i == "-noname":
      Qclustername = 0
      continue
    #PRESPLIT
    if i == "-presplit":
      last = "-presplit"
      continue
    if last == "-presplit":
      last = ""
      Qpresplit = int(i)
      continue
    # DROP
    if i == "-drop":
      last = "-drop"
      continue
    if last == "-drop":
      last = ""
      Qmodify = 1
      Qdrop = i
      continue
    #COMPLEMENT
    if i == "-complement":
      last = "-complement"
      continue
    if last == "-complement":
      last = ""
      Qcomplement = str(i)
      continue
    #INDEX
    if i == "-i" or i == "-index":
      last = "-index"
      continue
    if last == "-index":
      last = ""
      Qindex = str(i)
      continue
    #UNDERSCORE
    if i == "-underscore":
      Qmodify = 1
      Qunderscore = 1
      continue
    # OUT 2 LOG
    if i == "-out2log":
      Qout2log = 1
      Qmodify
      continue
    #RENAME
    if i == "-rename":
      Qmodify = 1
      Qrename = 1
      last = "-rename"
      continue
    if last == "-rename":
      remember = i
      last = "-rename2"
      continue
    if last == "-rename2":
      last = ""
      QrenameWHAT.append([remember,i])
      continue
    #rebasename
    if i == "-rebasename":
      Qrebasename = 1
      Qmodify = 1
      continue
    #REACTED
    if i == "-reacted":
      Qreacted = 1
    #  last = "-reacted"
      continue
    if i == "-reacted2":
      Qreacted = 2
    #  last = "-reacted"
      continue
    #if last == "-reacted":
    #  last = ""
    #  bonddistancethreshold = float(i)
    #  continue  
    #NOEXAMPLE
    if i == "-noexample" or i == "-noex":
      Qout = 0
      continue
    #TEST
    if i == "-test":
      Qout = 2
      continue
    #SPLIT
    if i == "-split":
      last = "-split"
      continue
    if last == "-split":
      Qsplit = int(i)
      last = ""
      continue
    #EXTRACT
    if i == "-extract":
      last = "-extract"
      continue
    if last == "-extract":
      last = ""
      Qextract = 1
      Pextract.append(i)
      continue
    #EXCEPT
    if i == "-except":
      last = "-except"
      continue
    if last == "-except":
      last = ""
      Qextract = 2
      Pextract.append(i)
      continue
    #INPUT FILES
    if len(i) > 3:
      ext = i[-4:]
      if ext == ".xyz" or ext == ".log" or ext == ".out":
        if path.exists(i):
          files.append(i)
          continue
        else:
          print("File "+i+" does not exist. Sorry [EXITING]")
          exit()
      if ext == ".pkl":
        if path.exists(i):
          input_pkl.append(i)
          continue
        else:
          if output_pkl != "mydatabase.pkl":
            print("Hey either one input database does not exist or you are trying to use two different outputs? "+output_pkl+"/"+i+" [EXITING]")
            exit()
          else:
            output_pkl = i
            continue
    ########
    # SORT 
    if i == "-sort" or i == "--sort":
      last = "-sort"
      continue
    if last == "-sort":
      last = ""
      Qsort = str(i)
      continue
    # SELECT
    if i == "-select" or i == "--select":
      last = "-select"
      continue
    if last == "-select":
      last = ""
      Qselect = int(i)
      continue  
    # SAMPLE
    if i == "-sample":
      last = "-sample"
      continue
    if last == "-sample":
      last = "-uniq"
      Qsample = int(i)
      continue
    # UNIQUE
    if i == "-unique" or i == "--unique" or i == "-uniq" or i == "--uniq":
      last = "-uniq"
      continue
    if last == "-uniq":
      last = ""
      Quniq = str(i)
      continue
    if i == "-is" or i == "-filter_==":
      Qthreshold = 1
      last = "-threshold"
      attach = ["==","absolute"]
      continue
    if i == "-isnot" or i == "-filter_ne":
      Qthreshold = 1
      last = "-threshold"
      attach = ["!=","absolute"]
      continue
    if i == "-cut" or i == "-filter_le":
      Qthreshold = 1
      last = "-threshold"
      attach = ["<=","absolute"]
      continue
    if i == "-filter_lt":
      Qthreshold = 1
      last = "-threshold"
      attach = ["<","absolute"]
      continue
    if i == "-rel_filter_lt":
      Qthreshold = 1
      last = "-threshold"
      attach = ["<","relative"]
      continue
    if i == "-cutr" or i == "-rel_filter_le":
      Qthreshold = 1
      last = "-threshold"
      attach = ["<=","relative"]
      continue
    if i == "-filter_le":
      Qthreshold = 1
      last = "-threshold"
      attach = ["<=","absolute"]
      continue
    if i == "-pass" or i == "-filter_gt":
      Qthreshold = 1
      last = "-threshold"
      attach = [">","absolute"]
      continue
    if i == "-filter_ge":
      Qthreshold = 1
      last = "-threshold"
      attach = [">=","absolute"]
      continue
    if i == "-passr" or i == "-rel_filter_gt":
      Qthreshold = 1
      last = "-threshold"
      attach = [">","relative"]
      continue
    if i == "-rel_filter_ge":
      Qthreshold = 1
      last = "-threshold"
      attach = [">=","relative"]
      continue
    #
    if last == "-threshold":
      if str(i) == "bonded":
        last = "-bonded_thr1"
      else:
        last = "-threshold2"
      attach.append(i)
      continue
    if last == "-threshold2":
      last = ""
      attach.append(str(i))
      Qcut.append(attach)
      continue
    #bonded threshold
    if last == "-bonded_thr1":
      last = "-bonded_thr2"
      rem = [str(i)]
      continue
    if last == "-bonded_thr2":
      last = "-bonded_thr3"
      rem.append(str(i))
      continue
    if last == "-bonded_thr3":
      last = "-threshold2"
      rem.append(str(i))
      attach.append(rem)
      rem = ""
      continue 
    #ArbAlign
    if i == "-arbalign" or i == "-ArbAlign":
      last = "-arbalign"
      continue
    if last == "-arbalign":
      last = ""
      Qarbalign = float(i)
      continue
    #SHUFFLE
    if i == "-shuffle":
      Qshuffle = 1
      continue
    ########
    # INFO
    if i == "-info" or i == "--info":
      Pout.append("-info")
      continue
    # CITE
    if i == "-cite" or i == "--cite":
      Pout.append("-cite")
      continue
    # ATOMS
    if i == "-atoms":
      Pout.append("-atoms")
      continue
    # XYZ
    if i == "-xyz" or i == "--xyz" or i == "-XYZ" or i == "--XYZ":
      Pout.append("-xyz")
      continue
    if i == "-imos" or i == "--imos" or i == "-IMOS" or i == "--IMOS" or i == "-IMoS" or i == "--IMoS":
      Pout.append("-imos")
      continue
    if i == "-imos_xlsx" or i == "--imos_xlsx":
      Pout.append("-imos_xlsx")
      continue
    # MOVIE
    if i == "-movie" or i == "--movie":
      Pout.append("-movie")
      continue
    # RG
    if i == "-rg" or i == "--rg" or i == "-Rg" or i == "--Rg":
      Pout.append("-rg")
      continue
    if i == "-radius" or i == "--radius":
      Pout.append("-radius")
      continue
    if i == "-radius0.5" or i == "--radius0.5":
      Pout.append("-radius0.5")
      continue
    # INFO
    if i == "-ct" or i == "-clustertype" or i == "--ct" or i == "--clustertype":
      Pout.append("-ct")
      continue
    if i == "-b" or i == "-basename" or i == "--b" or i == "--basename":
      Pout.append("-b")
      continue
    if i == "-nOUT" or i == "--nOUT":
      Pout.append("-nOUT")
      continue
    if i == "-nLOG" or i == "--nLOG":
      Pout.append("-nLOG")
      continue
    if i == "-nXYZ" or i == "--nXYZ":
      Pout.append("-nXYZ")
      continue
    if i == "-pOUT" or i == "--pOUT":
      Pout.append("-pOUT")
      continue
    if i == "-pLOG" or i == "--pLOG":
      Pout.append("-pLOG")
      continue
    if i == "-pXYZ" or i == "--pXYZ":
      Pout.append("-pXYZ")
      continue
    if i == "-ePKL" or i == "--ePKL":
      Pout.append("-ePKL")
      continue
    # LOG & OUT
    if i == "-elSP" or i == "-elsp" or i == "--elSP" or i == "--elsp":
      Pout.append("-elsp")
      continue
    if i == "-el" or i == "-elen" or i == "--el" or i == "--elen":
      Pout.append("-el")
      continue
    if i == "-elout" or i == "--elout":
      Pout.append("-elout")
      continue
    if i == "-elc" or i == "--elc":
      Pout.append("-elc")
      continue
    if i == "-g" or i == "-gibbs" or i == "--g" or i == "--gibbs":
      Pout.append("-g")
      continue
    if i == "-pop" or i == "--pop":
      Pout.append("-pop")
      continue
    if i == "-natoms":
      Pout.append("-natoms")
      continue
    if i == "-h" or i == "-enthalpy" or i == "--h" or i == "--enthalpy":
      Pout.append("-h")
      continue
    if i == "-s" or i == "-entropy" or i == "--s" or i == "--entropy":
      Pout.append("-s")
      continue
    if i == "-mass":
      Pout.append("-mass")
      continue
    if i == "-u" or i == "--u":
      Pout.append("-u")
      continue
    if i == "-uc" or i == "--uc":
      Pout.append("-uc")
      continue
    if i == "-uout" or i == "--uout":
      Pout.append("-uout")
      continue
    if i == "-hc" or i == "--hc":
      Pout.append("-hc")
      continue
    if i == "-hout" or i == "--hout":
      Pout.append("-hout")
      continue
    if i == "-gc" or i == "--gc":
      Pout.append("-gc")
      continue
    if i == "-g" or i == "--g" or i == "-gibbs" or i == "--gibbs" or i == "-G" or i == "--G":
      Pout.append("-g")
      continue
    if i == "-gout" or i == "--gout" or i == "-GDh" or i == "--GDh" or i == "-GD" or i == "--GD":
      Pout.append("-gout")
      continue
    if i == "-zpec" or i == "-zpecorr" or i == "--zpec" or i == "--zpecorr":
      Pout.append("-zpec")
      continue
    if i == "-zpe" or i == "-ZPE" or i == "--zpe" or i == "--ZPE":
      Pout.append("-zpe")
      continue
    if i == "-zpeout" or i == "-ZPEout" or i == "--zpeout" or i == "--ZPEout":
      Pout.append("-zpeout")
      continue
    if i == "-lf" or i == "-lfreq" or i == "--lf" or i == "--lfreq":
      Pout.append("-lf")
      continue
    if i == "-f" or i == "-freq" or i == "--f" or i == "--freq":
      Pout.append("-f")
      continue
    if i == "-rot" or i == "--rot":
      Pout.append("-rot")
      continue
    if i == "-rots" or i == "--rots":
      Pout.append("-rots")
      continue
    if i == "-mult" or i == "--mult":
      Pout.append("-mult")
      continue
    if i == "-char" or i == "-chrg" or i == "--char" or i == "--chrg":
      Pout.append("-char")
      continue
    if i == "-mull" or i == "--mull":
      Pout.append("-mull")
      continue
    if i == "-esp" or i == "--esp":
      Pout.append("-esp")
      continue
    if i == "-charges" or i == "--charges":
      Pout.append("-charges")
      continue
    if i == "-chargesESP" or i == "--chargesESP":
      Pout.append("-chargesESP")
      continue
    if i == "-dip" or i == "--dip":
      Pout.append("-dip")
      continue
    if i == "-dips" or i == "--dips":
      Pout.append("-dips")
      continue
    if i == "-pol" or i == "--pol":
      Pout.append("-pol")
      continue
    if i == "-templog" or i == "--templog":
      Pout.append("-templog")
      continue
    if i == "-preslog" or i == "--preslog":
      Pout.append("-preslog")
      continue
    if i == "-mi" or i == "--mi":
      Pout.append("-mi")
      continue
    if i == "-ami" or i == "--ami":
      Pout.append("-ami")
      continue
    if i == "-rsn" or i == "--rsn":
      Pout.append("-rsn")
      continue
    if i == "-level" or i == "-lvl":
      Pout.append("-level")
      continue
    if i == "-t" or i == "--t" or i == "-time" or i == "--time":
      Pout.append("-t")
      continue
    if i == "-termination" or i == "--termination":
      Pout.append("-termination")
      continue
    if i == "-extra":
      Pout.append("-extra")
      last = "-extra"
      continue
    if last == "-extra":
      last = ""
      Pout.append(str(i))
      continue
    #PRE_EXTRACT_DATA MANIPULATION
    if i == "-fc" or i == "--fc":
      Qqha = 1
      last = "-fc"
      continue
    if last == "-fc":
      last = ""
      Qfc = float(i)
      continue
    if i == "-temp" or i == "--temp":
      Qqha = 1
      last = "-temp"
      continue
    if last == "-temp":
      last = ""
      Qt = float(i)
      continue
    if i == "-as" or i == "--as" or i == "-v" or i == "--v":
      Qqha = 1
      last = "-as"
      continue
    if last == "-as":
      last = ""
      Qanh = str(i)
      continue
    if i == "-unit" or i == "--unit":
      QUenergy = 627.503
      QUentropy = 627503.0
      continue
    #FORMATION
    if i == "-glob" or i == "--glob":
      Qglob = 1
      continue
    if i == "-globout" or i == "--globout":
      Qglob = 2
      continue
    if i == "-bavg" or i == "--bavg":
      Qbavg = 1
      continue
    if i == "-bavgout" or i == "--bavgout":
      Qbavg = 2
      continue
    if i == "-formation" or i == "--formation":
      Qformation = 1
      continue
    if i == "-conc" or i == "--conc":
      Qconc = 1
      last = "-conc"
      continue
    if last == "-conc":
      last = "-conc2"
      remember = str(i)
      continue
    if last == "-conc2":
      last = ""
      from numpy import array
      conc.append(array([remember, i]))
      continue
    if path.exists(i):
      formation_input_file = i
      continue
    if i == "-cnt" or i == "--cnt":
      CNTfactor = 1
      continue
    #UNKNOWN ARGUMENT   
    print("I am sorry but I do not understand the argument: "+i+" [EXITING]")
    exit()  

  if last != "":
    print("Hey looser, the last argument is incomplete")
    exit()

  # CHECK WHICH FILES SHOULD BE LOADED
  if len(files) == 0:
    if len(input_pkl) == 0 and len(formation_input_file) == 0:
      from glob import glob
      if Qrecursive:
        files = glob(folder+"/**/*."+Qcollect, recursive = True)
      else:
        files = glob(folder+"/*."+Qcollect)
      del glob
      if len(files) == 0:
        print("No inputs. No *.log files. [EXITING]")
        exit()
    if len(input_pkl) == 1 and Qsplit != 1 and output_pkl == "mydatabase.pkl":
      output_pkl = input_pkl[0]
      if Qoutpkl == 0:
        Qoutpkl = 1
    if len(input_pkl) > 1:
      if Qoutpkl == 0:
        Qoutpkl = 1
  else:
    if len(Pout) == 0:
      if Qoutpkl == 0:
        Qoutpkl = 1
      print("Number of files: "+str(len(files)))
    else:
      if Qoutpkl == 0:
        Qoutpkl = 1

  del last,argument_list,path,missing,folder,Qcollect
  return locals()
