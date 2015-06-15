autocrab
========

NOTE: this documentation is all for the **CRAB 2** versions of AutoCrab, which
have now been rename to **autocrab2** and **autocrab2-newcfg**. CRAB 3 versions
are under active development.

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

If you want to run locally on condor, not remoteGlidein, pass "-c condor" (or 
"-c condor").

Example output dir: ``/eos/uscms/store/user/bjr/ntuples``

More documentation to follow.

## Using autocrab itself.

Autocrab is basically just a wrapper for a few crab commands; create/submit,
status/get all, status/resubmit bad, and publish.

However, it runs over all crab config files / working directories in a
directory. Example: assume you set up crab jobs crab_A.cfg and crab_B.cfg, then:

```autocrab create```

Will create and submit those jobs. Then:

```autocrab status```

Will run crab -status -get all" over both. Then, assuming some jobs failed:

```autocrab resubmit```

Will run crab -resubmit bad over both. And then, once you're done:

```autocrab publish```

Will publish both sets.

More advanced features to probably come.
