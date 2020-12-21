#!/usr/bin/env python

# Copyright (c) 2014, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: David Spears <dspears@paloaltonetworks.com>

"""
panorama-commit-push.py
==========

This script performs a panorama commit and will push to devices

**Usage**::

    upgrade.py [-h] [-v] [-q] [-n] hostname username password devicegroup

**Examples**:

Commit to a Panorama at 13.129.150.75 that has a modified devicegroup named GWLB:

    $ python pancommitandpush.py 13.129.150.75 username password GWLB

Instructions for installing the PAN-OS-SDK are located here:
https://pandevice.readthedocs.io/en/latest/getting-started.html

"""

__author__ = "dspears"


import argparse
from panos import panorama

def main():

    # Get command line arguments
    parser = argparse.ArgumentParser(
        description="Commit and Push an updated Panorama device group configuration"
    )
    parser.add_argument(
        "-v", "--verbose", action="count", help="Verbose (-vv for extra verbose)"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="No output")

    # Palo Alto Networks related arguments
    fw_group = parser.add_argument_group("Palo Alto Networks Device")
    fw_group.add_argument("hostname", help="Hostname of Panorama")
    fw_group.add_argument("username", help="Username for Panorama")
    fw_group.add_argument("password", help="Password for Panorama")
    fw_group.add_argument("devicegroup", help="DeviceGroup for Panorama")
    args = parser.parse_args()

    # Connects to Panorama.
    pano = panorama.Panorama(args.hostname, args.username, args.password,) # Create a panorama object
    # Performs the commit and device group push
    print("Performing commit...")
    pano.commit(sync_all=True,sync=True)
    print("Done")
    print("Performing device push...")
    pano.commit_all(sync=True,sync_all=True,cmd="<commit-all><shared-policy><device-group><entry name='%s'/></device-group></shared-policy></commit-all>"%(args.devicegroup))
    print("Done")
    
# Call the main() function to begin the program if not
# loaded as a module.
if __name__ == "__main__":
    main()