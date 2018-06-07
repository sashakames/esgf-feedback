import json, os, logging, sys

import addr_lookup
from email_sender import notify as email_notify


IN_PATH = '/tmp/feedback'
LOOK_PATH = IN_PATH + '.1'

JUNK_YARD = '/esg/log/feedback-failed'

LOG_FILE = '/esg/log/feedback.log'

user_dict = {}

out_log_arr = []





def format_email(user, user_action_dict):
    ''' 
    Arguments: (1) user name to address in email body; (2) a dictionary object (from json) dat structure that contains the datasets and respective update status, eg UPDATE or RETRACTION
    '''
# TODO format this for the user (decode the json)

    message = "Dear " + user + ": here's a notification email regarding status changes to datasets."

    outs = message + "\n" + json.dumps(user_action_dict)
    return outs


def process_users(user_dict, user_addr=False):

    for user in user_dict:

        user_items = user_dict[user]

        # Lookup user email - bulk query or single user?

        # for now hardcoded email
        
        user_action_dict = {}
        
        for its in user_items:

            action = its["update_status"]

            if action in user_action_dict:
                
                dset_lst = user_action_dict[action]
                dset_lst.append(its["master_id"])

            else:                
                user_action_dict[action] = [its["master_id"]]
        

            
#        dest_addr = addr_lookup.get(user)
        dest_addr = user
        subject = "ESGF Datatset status updates"

        body = format_email(user, user_action_dict)

        if (len(sys.argv) > 1 and sys.argv[1] == "--test"):
            print dest_addr, subject, body 
        else:
            email_notify(dest_addr, subject, body)



def main():

    logger = logging.getLogger('esgf-feedback')
    logger.setLevel(logging.WARNING)


    os.rename(IN_PATH, LOOK_PATH)

    os.mkdir(IN_PATH)

    files = os.listdir(LOOK_PATH)
#    files = os.listdir(IN_PATH)

    for ff in files:
        
        fpath = LOOK_PATH + '/' + ff
#        fpath = IN_PATH + '/' + ff
        jobj = None
        
        try:

            jobj = json.loads(open(fpath).read())
        except:
            logger.error("Error with json file: ")
            
            os.rename(fpath, JUNK_YARD + "/" + ff)

            continue
            
        for it in jobj:

            dset = it["dataset"]
            action = it["action"]

            for usr in it["users"]:
                record = { 'update_status': action , 'master_id': dset }               

                if usr in user_dict:

                    dset_lst = user_dict[usr]

                    dset_lst.append(record)
                    user_dict[usr] = dset_lst
                else:
                    user_dict[usr] = [record]


        out_log_arr.append(jobj)
        os.remove(LOOK_PATH + "/" + ff)


    process_users(user_dict)

    os.rmdir(LOOK_PATH)
    open(LOG_FILE, 'w').write(json.dumps(out_log_arr))

    return 0

if __name__ == "__main__":
    main()

