#!/usr/bin/env python3
# coding: utf-8

import sys


def hex_to_dec(filename):
    # Command prefix
    prefix = "sendevent"

    # Create output file, taking everything before the extension
    outfile = filename.rsplit('.', 1)[0] + ".sh"

    # Open the input and output files
    with open(filename, "r") as fo, open(outfile, "w") as fw:
        # Write the script header
        fw.write("#!/bin/sh\n")
        # fw.write("echo Running – drawing function\n")

        # Process each line in the input file
        for inputline in fo:
            # Find the location of the colon
            part1len = inputline.find(":")

            # If colon is found, process the line
            if part1len > -1:
                # Extract the device path
                part1 = inputline[:part1len].strip()

                # Split the line into parts and convert hex to decimal
                part2 = inputline[part1len + 1:].strip().split()
                if len(part2) >= 3:
                    try:
                        num1 = int(part2[0], 16)
                        num2 = int(part2[1], 16)
                        num3 = int(part2[2], 16)

                        # Assemble the new command
                        complete = f"{prefix} {part1} {num1} {num2} {num3}"

                        # Write the command to the output file
                        fw.write(complete + "\n")
                    except ValueError:
                        print(f"Skipping line due to conversion error: {inputline.strip()}")
                else:
                    print(f"Skipping line due to insufficient data: {inputline.strip()}")

    # Inform the user
    print("Processing complete")
    print(f"File created: {outfile}")
    print(f"Copy file to the device with: adb push {outfile} /sdcard/{outfile}")
    print(f"Run the script with: adb shell sh /sdcard/{outfile}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hex_to_dec.py <inputfile>")
        sys.exit(1)

    hex_to_dec(sys.argv[1])
