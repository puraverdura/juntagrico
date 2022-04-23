import copy
from django.utils import timezone
from django.core import mail
import time
import threading

class Mailer:

    def send(msg):

        def _send_batches(msg, email_batch_size, wait_time_batch):
            print('start sending')
            tos = msg.to
            ccs = msg.cc
            bccs = msg.bcc
            num_recipients = len(bccs) + len(tos) + len(ccs)
            recipients_batches = []
            if num_recipients <= email_batch_size:
                #print('send mail to:')
                #print(msg.recipients())
                msg.send()
                batch = {'timestamp': str(timezone.now()),'to': tos, 'cc': ccs, 'bcc': bccs}
                recipients_batches.append(batch)
                _send_admin_msg(msg, recipients_batches)
                return 

            plain_msg = copy.copy(msg)
            plain_msg.bcc = []

            t_wait = 0
            if tos or ccs:
                starttime = time.time()
                #print('send mail to:')
                #print(plain_msg.recipients())
                plain_msg.send()

                plain_msg.to = []
                plain_msg.cc = []

                batch = {'timestamp': str(timezone.now()), 'to': tos, 'cc': ccs, 'bcc': []}
                recipients_batches.append(batch)

                t_wait = wait_time_batch - (time.time() - starttime)

            if t_wait > 0:
                time.sleep(t_wait)
            
            for i in range(0, len(bccs), email_batch_size):
                starttime = time.time()
                batch_bccs = bccs[i:i + email_batch_size]
                
                new_message = copy.copy(plain_msg)
                new_message.bcc = batch_bccs
                #print('send mail to:')
                #print(new_message.recipients())
                new_message.send()
                
                batch = {'timestamp': str(timezone.now()), 'to': [], 'cc': [], 'bcc': batch_bccs}
                recipients_batches.append(batch)

                t_wait = wait_time_batch - (time.time() - starttime)
                if t_wait > 0:
                    print(f'wait for: {t_wait}s')
                    time.sleep(t_wait)

            _send_admin_msg(msg, recipients_batches)
            print()
            print('finished sending')

        def _send_admin_msg(msg, recipients_batches):
            admin_msg = copy.copy(msg)
            admin_msg.alternatives = []
            admin_msg.cc = []
            admin_msg.bcc = []
            admin_body = ''
            for batch in recipients_batches:
                admin_body = admin_body + str(batch) + ',\n\n'
            admin_msg.body = admin_body
            admin_msg.subject = f'[JUNTAGRICO] Email Recipients: {msg.subject}'
            admin_msg.to = ['it@puraverdura.ch']

            #print('send admin mail to:')
            #print(admin_msg.recipients())
            #print(admin_msg.subject)
            #print(admin_msg.body)
            admin_msg.send()
   

        email_batch_size = 39
        wait_time_batch = 65
        
        t = threading.Thread(target=_send_batches, args=[msg, email_batch_size, wait_time_batch], daemon=True)
        t.start()
        print('thread started')
       

