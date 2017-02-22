import json, os, logging

import addr_lookup
from email_sender import notify as email_notify


IN_PATH = '/tmp/feedback'
LOOK_PATH = IN_PATH + '.1'

JUNK_YARD = '/esg/log/feedback-failed'

LOG_FILE = '/esg/log/feedback.log'

user_dict = {}


def main():

    logger = logging.getLogger('esgf-feedback')
    logger.setLevel(logging.WARNING)


    os.rename(IN_PATH, LOOK_PATH)

    os.mkdir(IN_PATH)

    files = os.listdir(LOOK_PATH)

    for ff in files:
        
        fpath = LOOK_PATH + '/' + ff
        
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

                if usr in user_dict:

                    dset_lst = user_dict[usr]
                    dset_lst.append([dset, action])

                else:
                    user_dict[usr] = [dset, action]
    for user in user_dict:

        user_items = user_dict[user]

        # Lookup user email - bulk query or single user?

        # for now hardcoded email
        
        user_action_dict = {}

        for its in user_items:

            action = its[0]

            if action in user_action_dict:
                
                dset_lst = user_action_dict[action]
                dset_lst.append(its[1])

            else:                
                user_action_dict[action] = its[1]
        
            user_action_dict["Message"] = "Dear " + usr + ": here's a notification email regarding status changes to datasets."
            outs = json.dumps(user_action_dict)
            
            dest_addr = addr_lookup.get(usr)
            subject = "test"

            print dest_addr, subject, outs


    os.rmdir(LOOK_PATH)
    return 0

if __name__ == "__main__":
    main()
