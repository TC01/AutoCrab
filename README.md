autocrab
========

A collection of tools to automate running crab jobs for CMS analyses.

## Using autocrab-newcfg:

You can run the following command to get a DAS query:

``
das_client.py --limit=0 --query="QUERY"
``

This will output a list of dataset names that, coincidentally, are exactly the
right format for autocrab.

So run something like the following:

``
das_client.py --limit=0 --query="QUERY" > autocrab_mydataset.txt
``

Then, assuming you have a properly configured template.cfg in CWD:

``
autocrab-newcfg -o $OUTPUT_DIR -i autocrab_mydataset.txt
``

If running over data, pass the "-d" flag as well.

If you want scaleup/scaledown and smearup/smeardown, pass the "-s" and "-r" flags
respectively. This creates multiple crab config files.

If you want to run locally on condor, not remoteGlidein, pass "-c condor" (or "-c 

Example output dir: ``/eos/uscms/store/user/bjr/ntuples``

More documentation to follow.
