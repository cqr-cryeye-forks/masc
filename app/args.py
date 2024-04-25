import argparse
import pathlib


def init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output-file', type=pathlib.Path, help='Path to write output in json')

    parser.add_argument('-u', '--url', help='Add url: we get all files from here and send file to the Masc',
                        metavar='URL')

    parser.add_argument('-af', '--add-file', help='Add a suspect file to the dictionary', metavar='FILENAME')
    parser.add_argument('-aw', '--add-word', help='Add a suspect content to the dictionary', metavar='STRING')
    parser.add_argument('-cc', '--clean-cache', help='Clean masc cache (cache and logs files, NO backups)',
                        action='store_true')
    parser.add_argument('-c', '--clean-site',
                        help='Clean up the site (and apply some extra actions to hide information to attackers)',
                        action='store_true')
    parser.add_argument('-l', '--list-backups', help='List local backups', action='store_true')
    parser.add_argument('-b', '--make-backup', help='Create a local backup of the current installation',
                        action='store_true')
    parser.add_argument('-m', '--monitor', help='Monitor site to detect changes', action='store_true')
    parser.add_argument('-n', '--name', help='Name assigned to the scanned installation', metavar='NAME')
    parser.add_argument('-p', '--path', help='Website installation path', metavar='PATH')
    parser.add_argument('-r', '--rollback', help='Restore a local backup', action='store_true')
    parser.add_argument('-s', '--scan', help='Scan website for malware', action='store_true')
    parser.add_argument('-t', '--site-type',
                        help='which type of web you want to scan: wordpress, drupal or a custom website',
                        choices=['wordpress', 'drupal', 'custom'])
    args = parser.parse_args()
    return args
