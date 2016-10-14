
# A simple example showing a top level search on 
# LOCA's S3 cache copy. See http://loca.ucsd.edu 
# for the official distribution and general information.
# See the select_loca_data routine.


import urllib2, json, random

INVENTORY = 'http://nasanex.s3.amazonaws.com/LOCA/loca-s3-files.json'
MODELS = 'http://nasanex.s3.amazonaws.com/LOCA/models.json'

def get_json(ilink):
    return json.loads( urllib2.urlopen(ilink).read() )

def select_loca_data(jidx, model, vname, exprid, rtag, addhist=None):
    """Select LOCA S3 keys/files given a set of criteria.

        This routine builds a list of S3 keys, or web links, from the basic 
        LOCA json index. One might use this to determine an appropriate 
        listing of some model, ~experiment, variable name and resolution tag. 

    Args:
        jidx: The loaded json index from the LOCA S3 cache
        model: The name of the model of interest (see listing s3://nasanex/LOCA/models.json)
        vname: The variable of the model of interest (DTR, pr, tasmax, tasmin)
        exprid: The expriment id of interest, loosely defined here. Available 
                exprids are rcp45, rcp85, historical
        rtag: The resolution tag, 1x1 or 16th
        addhist: If this is not None then the history keys from model,vname,exprid,rtag
            will be prepended to the returned list.

    Returns:
        A list of LOCA keys/web links of interest
    """
    if addhist:
        l = [ k for k in jidx.keys() if jidx[k]['model'] == model and jidx[k]['variable'] == vname \
                  and (jidx[k]['experiment_id'] == exprid or jidx[k]['experiment_id'] == 'historical') and  \
                  jidx[k]['rtag'] == rtag ]
    else:
        l = [ k for k in jidx.keys() if jidx[k]['model'] == model and jidx[k]['variable'] == vname \
                  and jidx[k]['experiment_id'] == exprid and  jidx[k]['rtag'] == rtag ]
    l.sort()
    return  l


if __name__ == '__main__':
    idx = get_json(INVENTORY)
    models = get_json(MODELS)
    m = random.choice(models['models'])

    # find what we're after.
    kys = select_loca_data(idx, m, 'tasmax', 'rcp45', '16th', addhist=1)
    for k in kys:
        print k