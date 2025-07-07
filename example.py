# -*- coding: utf-8 -*-
# Pollux Labs
# polluxlabs.io

import time
import logging
# Import the previously created library
from rc522_spi_library import RC522SPILibrary, StatusCodes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    General example for reading the UID from any RFID card.
    """
    print("Starting the RFID Card Reader...")
    print("Hold any RFID card near the reader.")
    print("Press CTRL+C to exit.")

    reader = None
    try:
        # Initialize the library
        reader = RC522SPILibrary(rst_pin=22)
        
        # Stores the UID of the last seen card to prevent constant repetition
        last_uid = None

        while True:
            # 1. Scan for a card
            status, _ = reader.request()

            if status == StatusCodes.OK:
                # 2. If a card is in the field, get its UID (Anti-collision)
                status, uid = reader.anticoll()
                
                if status == StatusCodes.OK:
                    # Only act if it's a new card
                    if uid != last_uid:
                        last_uid = uid
                        
                        # Convert UID to a readable format
                        uid_str = ":".join([f"{i:02X}" for i in uid])
                        
                        print("\n================================")
                        print(f"Card detected!")
                        print(f"  UID: {uid_str}")
                        print("================================")
                        print("INFO: You can now use this UID in your own code.")
                # If the UID could not be read, but a card is present,
                # nothing is done until the card is removed.
            else:
                # 3. If no card is in the field anymore, reset `last_uid`
                if last_uid is not None:
                    print("\nCard removed. The reader is ready for the next card.")
                    last_uid = None

            # Short pause to reduce CPU load
            time.sleep(0.1)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        # Make sure to release the resources at the end
        if reader:
            reader.cleanup()
            print("RC522 resources released successfully.")

if __name__ == '__main__':
    main()
