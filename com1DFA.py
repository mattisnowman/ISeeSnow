from avaframe.com1DFA import com1DFA
from avaframe.in3Utils import cfgUtils, cfgHandling

def run(cfgMain, mu, xi, terrainGrid, releaseShape, releaseHeight=0):
	#++++++++++ Perform simulation with com1DFA module
	# get the configuration of com1DFA using overrides
	cfgCom1DFA = cfgUtils.getModuleConfig(com1DFA, fileOverride='', modInfo=False, toPrint=False, onlyDefault=True)
	cfgCom1DFA, cfgMain = cfgHandling.applyCfgOverride(cfgCom1DFA, cfgMain, com1DFA, addModValues=False)
	# call com1DFA and perform simulations
	dem, plotDict, reportDictList, simDF = com1DFA.com1DFAMain(cfgMain, cfgInfo=cfgCom1DFA)
	#+++++++++++++++++++++++++++++++++++++++++++++++

	print(dem)
	print(plotDict)
	print(reportDictList)
	print(simDF)

	return dem, plotDict, reportDictList, simDF
