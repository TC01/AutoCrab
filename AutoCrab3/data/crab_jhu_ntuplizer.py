# Taken from https://github.com/osherson/dfehling, modified for autocrab purposes.
# This is the 'default' AutoCrab3 config file.

# Configurable parameters that AutoCrab3 will modify.
dataset = '$DATASET_LONG'
name = '$DATASET_SHORT'
defaultParams = ['runOnData=0', 'JES=nominal', 'JER=nominal', 'includePDF=0', 'runOnCrab=1']
params = []

# The actual crab config file, written by Dave Fehling.
from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.transferOutputs = True
config.General.requestName = name

config.section_('JobType')
config.JobType.psetName = 'hadronic.py'
config.JobType.pluginName = 'Analysis'
config.JobType.inputFiles = ['JEC/START53_V27_L1FastJet_AK7PFchs.txt', 'JEC/START53_V27_L2Relative_AK7PFchs.txt', 'JEC/START53_V27_L3Absolute_AK7PFchs.txt', 'JEC/START53_V27_Uncertainty_AK7PFchs.txt',
								'JEC/START53_V27_L1FastJet_AK5PFchs.txt', 'JEC/START53_V27_L2Relative_AK5PFchs.txt', 'JEC/START53_V27_L3Absolute_AK5PFchs.txt', 'JEC/START53_V27_Uncertainty_AK5PFchs.txt',
								'JEC/Winter14_V5_DATA_L1FastJet_AK7PFchs.txt', 'JEC/Winter14_V5_DATA_L2Relative_AK7PFchs.txt', 'JEC/Winter14_V5_DATA_L3Absolute_AK7PFchs.txt',
								'JEC/Winter14_V5_DATA_L2L3Residual_AK7PFchs.txt', 'JEC/Winter14_V5_DATA_Uncertainty_AK7PFchs.txt',
								'JEC/Winter14_V5_DATA_L1FastJet_AK5PFchs.txt', 'JEC/Winter14_V5_DATA_L2Relative_AK5PFchs.txt', 'JEC/Winter14_V5_DATA_L3Absolute_AK5PFchs.txt',
								'JEC/Winter14_V5_DATA_L2L3Residual_AK5PFchs.txt', 'JEC/Winter14_V5_DATA_Uncertainty_AK5PFchs.txt']
config.JobType.pyCfgParams = [params]

config.section_('Data')
config.Data.inputDataset = dataset
config.Data.unitsPerJob = 5
config.Data.splitting = 'FileBased'
config.Data.publishDataName = name

config.section_('User')

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
