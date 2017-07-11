from ftplib import FTP
from ftplib import error_perm
import getpass
import hashlib


class FtpResolver(object):

    def __init__(self, server):
        self.server = server

    def resolve(self):
        ftp = FTP()

        server = {'host': 'win1.chocolate-cloud.dk', 'port':21}
        connected = False

        while not connected:
            try:
                user = raw_input('Username for the %s server: ' % name)
                password = getpass.getpass('Password for the %s server: ' % name)

                ftp.connect(server)
                ftp.login(user, password)
            except error_perm:
                print('Log in failed! Incorrect username and/or password.')
            else:
                print('Log in succeeds!')
                connected = True

        # Use the first 6 characters of the SHA1 hash of the repository url
        # to uniquely identify the repository
        source_hash = hashlib.sha1(self.source.encode('utf-8')).hexdigest()[:6]

        # The folder for storing the file
        folder_name = 'ftp-' + source_hash
        folder_path = os.path.join(self.cwd, folder_name)

        ftp.retrbinary('RETR ' + self.source,
                       open(os.path.join(folder_path, "test.txt"), 'wb').write)

        return folder_path
