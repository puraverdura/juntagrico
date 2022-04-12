import copy
import time

class Mailer:
    def send(msg):
        starttime = time.time()
        bccs = msg.bcc
        email_batch_size = 3
        num_bccs = len(bccs)
        if num_bccs <= email_batch_size:
            #print('send mail to:')
            #print(msg.recipients())
            msg.send()
            mails_duration = time.time() - starttime
            print(f'Mailer sent {num_bccs} Mails in {mails_duration:.3f} seconds')
            return

        plain_msg = copy.copy(msg)
        plain_msg.bcc = []

        if msg.to or msg.cc:
            #print('send mail to:')
            #print(plain_msg.recipients())
            plain_msg.send()
            plain_msg.to = []
            plain_msg.cc = []

        for i in range(0, num_bccs, email_batch_size):
            batch_bccs = bccs[i:i + email_batch_size]
            new_message = copy.copy(plain_msg)
            new_message.bcc = batch_bccs
            #print('send mail to:')
            #print(new_message.recipients())
            new_message.send()

        mails_duration = time.time() - starttime
        print(f'Mailer sent {num_bccs} Mails in {mails_duration:.3f} seconds')

        admin_msg = copy.copy(plain_msg)
        admin_msg.body = str(bccs)
        admin_msg.to = ['it@puraverdura.ch']
        #print('send mail to:')
        #print(admin_msg.recipients())
        admin_msg.send()

