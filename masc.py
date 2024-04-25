#!/usr/bin/python3
import json
import os
import pathlib
import sys

from progress.spinner import Spinner
from termcolor import colored

from Constants import LOGS_DIR, PATH_TO_CONTENT_FOLDER, result_dict
from Custom import Custom
from Dictionary import Dictionary
from Drupal import Drupal
from MascUtils import MascUtils, BACKUPS_DIR
from PrintUtils import print_green, print_blue, print_red, print_info, print_results
from Wordpress import Wordpress
from args import init_args
from get_links import get_links
from load_links import load_links


def main():
    # CWD = os.getcwd() + '/'

    # Print some info about masc (version, github site, . . .)
    print_info()
    output_file = ''

    if len(sys.argv) == 1:
        print("No arguments provided. Execute '" + sys.argv[0] + " -h' for help")
        exit()

    args = init_args()

    if args.url:
        get_links(url=args.url)
        load_links()
        args.path = PATH_TO_CONTENT_FOLDER

    if args.output_file:
        output_file = pathlib.Path(args.output_file)

    if args.scan:

        if not args.path:
            print_red("You must specify the installation path to perform a scan")
            exit()

        if not args.site_type:
            print_red("You must specify the installation type to perform a scan")
            exit()

        if args.clean_site and not args.name:
            print_red("You selected clean up your website, but no name was provided. " +
                      "You must choose a name if you want to clean up your site")
            exit()

        # Set a default or choosen name
        name = 'no_name'
        if args.name:
            name = args.name

        cms = None
        try:
            if args.site_type == 'wordpress':
                cms = Wordpress(args.path, name)
            elif args.site_type == 'drupal':
                cms = Drupal(args.path, name)
            elif args.site_type == 'custom':
                cms = Custom(args.path, name)
        except Exception as e:
            print_red(e)
            print_blue("Exiting . . .")
            exit()

        # Load dictionaries/signatures/rules from databases
        print_blue("Loading dictionaries and signatures. . . ")
        Dictionary.load_suspect_files(args.site_type, args.path)
        Dictionary.load_suspect_content(args.site_type, args.path)
        Dictionary.load_signatures()
        print_green("Done.")

        # Scan and load some information about the website
        print_blue("Loading web site . . . ")
        cms.scan()
        print_green("Done.")

        # First, it makes a complete backup of the website (user can rollback later if masc clean too agressive)
        print_blue("Making a backup . . .")
        if not cms.make_backup():
            print_red("An error has occured while making backup. Aborting . . .")
            exit()
        print_green("Done.")

        # TODO: attention! In Natrix we use only 'custom' type, so i make saving output only to it.
        # If user chosen custom website, masc only try to search and print some info. Then, exit
        if args.site_type == "custom":
            print_blue("Searching for malware . . .")
            results = cms.search_malware_signatures()
            print_results(results)
            print_green("Done.")

            if output_file:
                if 'message' not in result_dict:
                    result_dict['message'] = "Site down or check ended with error"
                json_data = json.dumps(result_dict)
                output_file.write_text(json_data)
                print(f"Final results save to {output_file.absolute().as_uri()}")

            exit()

        # Compare malware and suspect files with clean installation files
        print_blue("Let's search for malware and suspect files. Then, let's compare results with a clean installation")
        files_to_remove = cms.compare_with_clean_installation()
        if len(files_to_remove) == 0:
            print_green("No malware/suspect files were found. Congratulations! Your website seems to be clear")

        # If the user didn't choose clean the site, masc only show which files may be infected
        if not args.clean_site:
            if len(files_to_remove) > 0:
                print_red(
                    "Malware/suspect files were found. They will be removed if you include the option --clean-site")
                for filename in files_to_remove:
                    print("\t" + os.path.join(cms.path, filename))
            exit()

        # The user chose clean up the site
        if args.clean_site:
            try:
                if len(files_to_remove) > 0:
                    # Remove malware/suspect files
                    spinner = Spinner(colored("Malware/suspect files were found. Removing . . .", "red"))
                    for filename in files_to_remove:
                        # FIXME Sometimes a directory is listed
                        if os.path.isdir(os.path.join(cms.path, filename)):
                            continue

                        os.remove(os.path.join(cms.path, filename))
                        cms.log.info("malware/suspect file removed:" + os.path.join(cms.path, filename))
                    print()
                    print_green("Done.")

                # Perform some cleaning up operations to hide some info about the site (at this moment only available
                # for wordpress)
                print_blue("Cleaning site . . .")
                cms.cleanup_site()
                print_green("Done.")

                print_blue("Some changes can have occured. See log '" + LOGS_DIR + cms.get_log_name() +
                           "'{%date} for details")
            except Exception as e:
                print(e)

    # User chose list backups
    elif args.list_backups:
        print_blue("Listing local backups . . .")
        MascUtils.list_backups()
        print_green("Done.")

    # User chose make a backup
    elif args.make_backup:

        if not args.path:
            print_red("You must provide the path of your website to make a backup")
            exit()

        if not args.site_type:
            print_red("You must provide the type-site option to make a backup")
            exit

        if not args.name:
            print_red("You must provide the name of your installation to make a backup")
            exit()

        # Check if it's exists a previous backup of the same website for the same date
        backups_list = os.scandir(BACKUPS_DIR)
        found = False
        for backup in backups_list:
            backup_parts = backup.name.split("_")
            # List dates from previous backup if found
            if backup_parts[0] == args.name:
                if not found:
                    print_blue("There is a previous backup with the same name")
                    found = True
                print_blue("\t" + backup_parts[1])

        # Some previous backups were found
        if found:
            print_blue("What do you want to do? [m]ake backup/[C]ancel")
            user_input = input('')
            if user_input != 'm':
                print_red('Aborted by user.')
                exit()

        print_blue("Making backup . . .")
        website = Custom(args.path, args.name, args.site_type)
        website.make_backup()
        print_green("Done.")

    # User choose restore the website with a previous backup
    elif args.rollback:
        if not args.path:
            print_red("You must provide the path of your website to rollback")
            exit()

        if not args.site_type:
            print_red("You must provide the type-site option to rollback")
            exit

        if not args.name:
            print_red("You must provide the name of your installation to rollback")
            exit()

        print_blue("Restoring backup . . .")
        website = Custom(args.path, args.name, args.site_type)
        website.rollback_backup()
        print_green("Done.")

    # User chose clean masc cache (logs and cache dirs)
    elif args.clean_cache:
        print_blue("Cleaning masc cache . . .")
        MascUtils.clean_cache()
        print_green("Done.")

    # User chose monitor current installation
    elif args.monitor:
        if not args.path:
            print_red("You must provide the path of your website to monitor it")
            exit()

        if not args.site_type:
            print_red("You must provide the type-site option to monitor it")
            exit()

        if not args.name:
            print_red("You must provide the name of your installation to monitor it")
            exit()

        print_blue("Monitoring website . . .(Press CTRL+C to terminate)")
        website = Custom(args.path, args.name, args.site_type, False)
        website.monitor()
        print_green("Finished")

    elif args.add_file:
        if not args.site_type:
            print_red("You must specify the site_type to add a new suspect file")
            exit()

        Dictionary.add_suspect_file(args.site_type, args.add_file)
        print_blue("Added '" + args.add_file + "' as a suspect file to the " + args.site_type + " dictionary")
    elif args.add_word:
        if not args.site_type:
            print_red("Yoy must specify the site_type to add a new suspect content")
            exit()

        Dictionary.add_suspect_content(args.site_type, args.add_word)
        print_blue("Added '" + args.add_word + "' as a suspect word to the " + args.site_type + " dictionary")
    else:
        print("No option provided. Try execute '" + sys.argv[0] + " -h' for help")


if __name__ == "__main__":
    main()
