import MadGraphControl.MadGraph_NNPDF30NLO_Base_Fragment
from MadGraphControl.MadGraphUtils import *
import re
import math, cmath
import os

nevents=runArgs.maxEvents

bonus_file = open('pdg_extras.dat','w')
#s-channel specific  
bonus_file.write('9000002\n')
bonus_file.write('9000003\n')
bonus_file.write('9000004\n')
bonus_file.write('-9000002\n')
bonus_file.write('-9000003\n')
bonus_file.write('-9000004\n')
bonus_file.close()
testSeq.TestHepMC.UnknownPDGIDFile = 'pdg_extras.dat'

print "ARGS: ", runArgs.jobConfig[0]
Mz = float(jofile.rstrip('.py').split('_')[2])
Rinv = float(jofile.rstrip('.py').split('_')[3])/10
print("Mz ", Mz)
print("Rinv ", Rinv)

masses={
    '1000022': str(10),
    '5000001': str(Mz)
}

decays={
    '5000001': 'auto'
}

params={'MASS':masses,
        'DECAY':decays}

my_process = """
import model  DMsimp_s_spin1 --modelname
define j = g u c d b t s u~ c~ d~ b~ s~ t~
generate p p > xd xd~ 
add process p p > xd xd~ j 
add process p p > xd xd~ j j
output -f
"""

run_settings = {'xqcut':100, 
               'nevents':int(nevents)
                }

process_dir = new_process(my_process)
runName='run_01'

modify_param_card(process_dir=process_dir,params=params)
modify_run_card(process_dir=process_dir,runArgs=runArgs,settings=run_settings)
generate(process_dir=process_dir,runArgs=runArgs)

unzip1 = subprocess.Popen(['gunzip',process_dir+'/Events/'+runName+'/unweighted_events.lhe.gz'])
unzip1.wait()
oldlhe = open(process_dir+'/Events/'+runName+'/unweighted_events.lhe','r')
newlhe = open(process_dir+'/Events/'+runName+'/unweighted_events2.lhe','w')
init = True
for line in oldlhe:
            if '1000022' in line:
                line = line.replace('1000022','4900101')                           
            newlhe.write(line)
oldlhe.close()
newlhe.close()
zip1 = subprocess.Popen(['gzip',process_dir+'/Events/'+runName+'/unweighted_events2.lhe'])
zip1.wait()
shutil.move(process_dir+'/Events/'+runName+'/unweighted_events2.lhe.gz',process_dir+'/Events/'+runName+'/unweighted_events.lhe.gz')
os.remove(process_dir+'/Events/'+runName+'/unweighted_events.lhe')
outDS = arrange_output(process_dir=process_dir,runArgs=runArgs,lhe_version=3)

# Go to serial mode for Pythia8
if 'ATHENA_PROC_NUMBER' in os.environ:
    print 'You run with an athena MP-like whole-node setup. Re-configureing to run remainder of the job serially.'
    njobs = os.environ.pop('ATHENA_PROC_NUMBER')
    # Try to modify the opts underfoot
    if not hasattr(opts,'nprocs'): print 'Did not see option!'
    else: opts.nprocs = 0
    print opts

runArgs.inputGeneratorFile = outDS

#### Shower 
evgenConfig.description = "Semivisible jets s-chan"
evgenConfig.keywords+=['BSM','sChannel']
evgenConfig.generators+=["MadGraph","Pythia8","EvtGen"]
evgenConfig.contact  = ['bingxuan.liu@cern.ch']
evgenConfig.process = "p p --> xd xd~ j j"

include("Pythia8_i/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")
include("Pythia8_i/Pythia8_MadGraph.py")

genSeq.Pythia8.Commands += ["JetMatching:merge = on"]
genSeq.Pythia8.Commands += ["JetMatching:scheme = 1"]
genSeq.Pythia8.Commands += ["JetMatching:setMad = on"]
genSeq.Pythia8.Commands += ["Check:epTolErr = 1e-2"]
genSeq.Pythia8.Commands += ["JetMatching:nJetMax = 2"]
genSeq.Pythia8.Commands += ["JetMatching:coneRadius = 0.4"]
genSeq.Pythia8.Commands += ["JetMatching:etaJetMax = 10.0"]

if "UserHooks" in genSeq.Pythia8.__slots__.keys():
  genSeq.Pythia8.UserHooks += ['JetMatchingMadgraph']
else:
  genSeq.Pythia8.UserHook = 'JetMatchingMadgraph'

genSeq.Pythia8.Commands+=["HiddenValley:Ngauge  = 2"]
genSeq.Pythia8.Commands+=["HiddenValley:spinFv = 0"]
genSeq.Pythia8.Commands+=["HiddenValley:FSR = on"]
genSeq.Pythia8.Commands+=["HiddenValley:fragment = on"]
genSeq.Pythia8.Commands+=["HiddenValley:alphaOrder = 1"]
genSeq.Pythia8.Commands+=["HiddenValley:Lambda = 0.1"]
genSeq.Pythia8.Commands+=["HiddenValley:pTminFSR = 1.1"]
genSeq.Pythia8.Commands+=["HiddenValley:probVector = 0.75"]

genSeq.Pythia8.Commands+=["4900001:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900002:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900003:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900004:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900005:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900006:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900011:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900012:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900013:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900014:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900015:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900016:m0 = 5000"]
genSeq.Pythia8.Commands+=["4900101:m0 = 10"]
genSeq.Pythia8.Commands+=["4900101:mWidth = 0.2"]
genSeq.Pythia8.Commands+=["4900101:mMin = 9.8"]
genSeq.Pythia8.Commands+=["4900101:mMax = 10.2"]
genSeq.Pythia8.Commands+=["4900111:m0 = 20.0"]
genSeq.Pythia8.Commands+=["4900113:m0 = 20.0"]
genSeq.Pythia8.Commands+=["51:m0 = 9.99"]
genSeq.Pythia8.Commands+=["53:m0 = 9.99"]
#s-channel specific
genSeq.Pythia8.Commands+=["4900211:m0 = 20.0"]
genSeq.Pythia8.Commands+=["4900213:m0 = 20.0"]

genSeq.Pythia8.Commands+=["4900111:onechannel = 1 {0} 91 -3 3".format(1 - Rinv)] # check Rinv syntax
genSeq.Pythia8.Commands+=["4900111:addchannel = 1 {0} 0 12 -12".format(Rinv)]

genSeq.Pythia8.Commands+=["4900113:onechannel = 1 {0}  91 -1 1".format((1-Rinv)/5)] 
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0}  91 -2 2".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0}  91 -3 3".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0}  91 -4 4".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0}  91 -5 5".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900113:addchannel = 1 {0} 0 12 -12".format(Rinv)] 

#s-channel specific
genSeq.Pythia8.Commands+=["4900211:onechannel = 1 {0} 91 -3 3".format(1 - Rinv)] # check Rinv syntax
genSeq.Pythia8.Commands+=["4900211:addchannel = 1 {0} 0 12 -12".format(Rinv)]
genSeq.Pythia8.Commands+=["4900213:onechannel = 1 {0}  91 -1 1".format((1-Rinv)/5)] 
genSeq.Pythia8.Commands+=["4900213:addchannel = 1 {0}  91 -2 2".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900213:addchannel = 1 {0}  91 -3 3".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900213:addchannel = 1 {0}  91 -4 4".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900213:addchannel = 1 {0}  91 -5 5".format((1-Rinv)/5)]
genSeq.Pythia8.Commands+=["4900213:addchannel = 1 {0} 0 12 -12".format(Rinv)] 

