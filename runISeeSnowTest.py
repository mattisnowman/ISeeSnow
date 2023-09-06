"""
    Run script for performing ISeeSnow test cases
    chose the test case by setting the parameter testCase in line 24 and additional settings in the following lines 
    the test case configuration is read from the respective test case's configuration file: 'ISeeSnowCfg%s.ini' % testCase
"""

# Load modules
import pathlib
import pandas as pd

# Local imports
import avaframe.in3Utils.initializeProject as initProj
from avaframe.com1DFA import com1DFA
from avaframe.in3Utils import cfgUtils, cfgHandling
from avaframe.in3Utils import logUtils
from avaframe.in3Utils import generateTopo
from avaframe.in3Utils import getReleaseArea
from avaframe.in1Data import getInput
from avaframe.runScripts.runAna3AIMEC import runAna3AIMEC
from avaframe.ana3AIMEC import ana3AIMEC


# +++++++++SETUP CONFIGURATION++++++++++++++++++++++++
# choose test case - options: IdealizedTopo, RealTopo, CoulombOnly
testCase = 'RealTopo'
runComputationalModule = True
comMod = 'com1DFA'
aimecDir = ''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++

# Load avalanche directory from general configuration file
dirPath = pathlib.Path(__file__).parents[0]
cfgMain = cfgUtils.getGeneralConfig(dirPath / ('ISeeSnowCfg%s.ini' % testCase))
avalancheDir = cfgMain['MAIN']['avalancheDir']

#+++++++++++++++ Initialize project with directory structure
initProj.initializeFolderStruct(avalancheDir)
# Start logging
logName = 'runISeeSnow_%s' % testCase
log = logUtils.initiateLogger(avalancheDir, logName)
log.info('MAIN SCRIPT')
log.info('Current avalanche: %s', avalancheDir)


if testCase in ['IdealizedTopo', 'CoulombOnly']:
    #+++++++++ Geometry generation +++++++++++++++++
    # get the configuration of generateTopo and getReleaseArea using overrides
    cfgGeo = cfgUtils.getModuleConfig(generateTopo, toPrint=False, onlyDefault=True)
    cfgGeo, cfgMain = cfgHandling.applyCfgOverride(cfgGeo, cfgMain, generateTopo)
    cfgRel = cfgUtils.getModuleConfig(getReleaseArea, toPrint=False, onlyDefault=True)
    cfgRel, cfgMain = cfgHandling.applyCfgOverride(cfgRel, cfgMain, getReleaseArea)

    # Call main function to generate DEM
    [z, name_ext, outDir] = generateTopo.generateTopo(cfgGeo, avalancheDir)
    # Call main function to generate release area
    [xv, yv, xyPoints] = getReleaseArea.getReleaseArea(cfgGeo, cfgRel, avalancheDir)

#++++++++++FETCH INPUT DATA++++++++++++++++++++++++++
# fetch file paths to input data: dem, release area
demFile, releaseFiles, releaseFields = getInput.getInputPaths(avalancheDir)
# only use first item of releaseFiles/releaseFields list - as we only have one release area shp/asc file in the input data
releaseFile = releaseFiles[0]
releaseField = releaseFields[0]
# get pandas dataFrame of friction model parameters
frictFile = dirPath / 'frictionParameterValues.csv'
frictionParameters = pd.read_csv(frictFile, header=0)
log.info('Fetched input data, dem: %s, release area: %s' % (demFile.stem, releaseFile.stem))

# ++++++++++CALL TO COMPUTATIONAL MODULE++++++++++++++
# HERE YOU COULD CALL YOUR MODULE
if runComputationalModule:
    if comMod == 'com1DFA':
        #++++++++++ Perform simulation with com1DFA module
        # get the configuration of com1DFA using overrides
        cfgCom1DFA = cfgUtils.getModuleConfig(com1DFA, fileOverride='', modInfo=False, toPrint=False, onlyDefault=True)
        cfgCom1DFA, cfgMain = cfgHandling.applyCfgOverride(cfgCom1DFA, cfgMain, com1DFA, addModValues=False)
        # call com1DFA and perform simulations
        dem, plotDict, reportDictList, simDF = com1DFA.com1DFAMain(cfgMain, cfgInfo=cfgCom1DFA)
        #+++++++++++++++++++++++++++++++++++++++++++++++
    else:
        log.error('ComMod: %s not available - consider implementing it :)' % comMod)

#++++++++++ Perform result analysis (based on aimec)+++++++++++++++++++++++
# OUTPUTS need to be located at aimecDir (if provided) or if aimecDir= '' files need to be located in avalancheDir/Outputs/comMod/peakFiles
# get the configuration of aimec using overrides
cfgAimec = cfgUtils.getModuleConfig(ana3AIMEC, fileOverride='', modInfo=False, toPrint=False, onlyDefault=True)
cfgAimec, cfgMain = cfgHandling.applyCfgOverride(cfgAimec, cfgMain, ana3AIMEC, addModValues=False)
# set anaMod 
cfgAimec['AIMECSETUP']['anaMod'] = comMod
runAna3AIMEC(avalancheDir, cfgAimec, inputDir=aimecDir)
log.info('Result analysis using ana3AIMEC performed')
log.info('ISeeSnow testcase: %s completed' % (testCase))
