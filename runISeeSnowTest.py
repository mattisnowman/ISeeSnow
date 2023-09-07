"""
    Run script for performing ISeeSnow test cases
    chose the test case by setting the parameter testCase in line 24 and additional settings in the following lines 
    the test case configuration is read from the respective test case's configuration file: 'ISeeSnowCfg%s.ini' % testCase
"""

# Load modules
import pathlib
import pandas as pd
import argparse

# Local imports
import avaframe.in3Utils.initializeProject as initProj
from avaframe.in3Utils import cfgUtils, cfgHandling
from avaframe.in3Utils import logUtils
from avaframe.in3Utils import generateTopo
from avaframe.in3Utils import getReleaseArea
from avaframe.in1Data import getInput
from avaframe.runScripts.runAna3AIMEC import runAna3AIMEC
from avaframe.ana3AIMEC import ana3AIMEC



# +++++++++SETUP CONFIGURATION++++++++++++++++++++++++
# choose test case - options: IdealizedTopo, RealTopo, CoulombOnly

parser = argparse.ArgumentParser(
                    prog = 'runISeeSnowTest.py',
                    description = 'Run script for performing ISeeSnow test case',
                )
parser.add_argument('--testCase', type = str, help = 'Select the test case [IdealizedTopo, RealTopo, CoulombOnly]', default = 'RealTopo')
parser.add_argument('--comMod', type = str, help = 'Select the backend. Should be available as a module.', default = 'com1DFA')
parser.add_argument('--runAimec', type = bool, help = 'Postprocess simulation results with AIMEC')


args = parser.parse_args()

testCase = args.testCase
comMod = args.comMod

# ++++++++++++++++++++++++++++++++++++++++++++++++++++

runComputationalModule = True
aimecDir = ''

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
if runComputationalModule:
    try: 
        model = __import__(comMod)
    except ImportError as ierr:
        log.error('ComMod: %s import error: %s - consider implementing it.' % (comMod, ierr.what))
    
    mu = cfgMain._sections['com1DFA_override']['muvoellmy']
    xi = cfgMain._sections['com1DFA_override']['xsivoellmy']
    h0 = cfgMain._sections['com1DFA_override']['relTh']

    if cfgMain._sections['com1DFA_override']['relThFromShp'] == 'False':
        dem, plotDict, reportDictList, simDF = model.run(cfgMain, mu, xi, demFile, releaseFields)
    else:
        dem, plotDict, reportDictList, simDF = model.run(cfgMain, mu, xi, demFile, releaseFiles, h0)


#++++++++++ Perform result analysis (based on aimec)+++++++++++++++++++++++
# OUTPUTS need to be located at aimecDir (if provided) or if aimecDir= '' files need to be located in avalancheDir/Outputs/comMod/peakFiles
# get the configuration of aimec using overrides
if args.runAimec:
    cfgAimec = cfgUtils.getModuleConfig(ana3AIMEC, fileOverride='', modInfo=False, toPrint=False, onlyDefault=True)
    cfgAimec, cfgMain = cfgHandling.applyCfgOverride(cfgAimec, cfgMain, ana3AIMEC, addModValues=False)
    # set anaMod 
    cfgAimec['AIMECSETUP']['anaMod'] = comMod
    runAna3AIMEC(avalancheDir, cfgAimec, inputDir=aimecDir)
    log.info('Result analysis using ana3AIMEC performed')
    log.info('ISeeSnow testcase: %s completed' % (testCase))
