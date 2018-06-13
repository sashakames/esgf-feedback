# for now a hardcoded dictionary
from sqlalchemy import create_engine
# from site_profile import get_prop_st


PASS_FN = '/esg/config/.esg_pg_pass'

db_engine = None
has_db = False

def  init_db():
    
    if not os.path.exists(PASS_FN):
        return (False, None)
    
    f = open(PASS_FN)

    passwd = f.read().strip()
    
#    properties_obj = get_prop_st()

    # Defaults based on conventional node installation

    db_user = 'dbsuper'  # properties_obj.get('db.user', 'dbsuper')
    db_host = 'localhost' # properties_obj.get('db.host', 'localhost')
    db_port = '5432' # properties_obj.get('db.port', '5432')
    db_database = 'esgcet' # properties_obj.get('db.database', 'esgcet')
    db_str = ( 'postgresql://' + db_user +  ':' + passwd + '@' + db_host  +  ':' + db_port+ '/' + db_database)

    engine = create_engine(db_str)

    return True, engine



#dct = { 'sashatest1': 'amysash2006@gmail.com', 'sashatest2': 'ames4@llnl.gov', 'sashatest3': 'sashakames@gmail.com'}

def get(k):


	if not has_db:
		return None


	qstr = "SELECT email FROM esgf_security_user WHERE username = '+k+'"

	ret_addr = None
	db_result = []

	try:
		db_result = db_engine.execute(qstr)
	except:
		return

	for row in db_result:
		ret_addr = row[0]
		if len(ret_addr) > 0:
			break

	return ret_addr
 #   return dct[k]
