import copy
from django.utils import timezone

class Mailer:
    def send(msg):
        bccs = msg.bcc
        email_batch_size = 3
        num_bccs = len(bccs)
        if num_bccs <= email_batch_size:
            #print('send mail to:')
            #print(msg.recipients())
            msg.send()
            return

        plain_msg = copy.copy(msg)
        plain_msg.bcc = []

        if msg.to or msg.cc:
            #print('send mail to:')
            #print(plain_msg.recipients())
            plain_msg.send()
            plain_msg.to = []
            plain_msg.cc = []

        bcc_list_of_lists = []
        timestamps = []
        for i in range(0, num_bccs, email_batch_size):
            timestamps.append(timezone.now())
            batch_bccs = bccs[i:i + email_batch_size]
            bcc_list_of_lists.append(batch_bccs)
            new_message = copy.copy(plain_msg)
            new_message.bcc = batch_bccs
            #print('send mail to:')
            #print(new_message.recipients())
            new_message.send()


        admin_msg = copy.copy(plain_msg)
        admin_msg.alternatives = []
        admin_body = ''
        for bcc_list, t in zip(bcc_list_of_lists, timestamps):
            admin_body = admin_body + str(t) + ': ' + str(bcc_list) + ',\n'
        admin_msg.body = admin_body
        admin_msg.to = ['it@puraverdura.ch']

        #print(admin_msg.body)
        #print('send mail to:')
        #print(admin_msg.recipients())
        admin_msg.send()

