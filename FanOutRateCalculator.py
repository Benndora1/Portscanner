from threading import Thread
from time import time

class FanOutRateCalculator(Thread):

    def __init__(self, first_contacts, lock):
        super().__init__()
        self.first_contacts = first_contacts
        self.lock = lock
        self.is_running = True

    def run(self):
        # List of time periods in seconds to calculate fan-out rates over
        ages = [1, 60, 300]
        # List of maximum fan-out rates allowed for each time period
        max_connections = [5, 100, 300]
        # Dictionary of IP addresses and time periods that have been blacklisted due to exceeding max fan-out rates
        blacklist = {}

        while self.is_running:
            # Dictionary to track fan-out rates for each source IP address
            source_connections = {}

            with self.lock:
                current_time = time()

                for key in self.first_contacts.keys():
                    source = key[0]

                    for i in range(len(ages)):
                        # Check if the key is within the current time period
                        if current_time - self.first_contacts[key] < ages[i]:
                            # Get the current fan-out rates for the source IP address or set to 0
                            fan_out_rates = source_connections.get(source, [0, 0, 0])
                            # Increment the fan-out rate for the current time period
                            fan_out_rates[i] += 1
                            # Update the fan-out rate for the source IP address
                            source_connections[source] = fan_out_rates

            # Check if any source IP addresses have exceeded max fan-out rates
            for key in source_connections.keys():
                detected = False
                reason = ''

                for i in range(len(max_connections)):
                    # Check if the fan-out rate for the current time period has exceeded the max allowed
                    if source_connections[key][i] > max_connections[i]:
                        # Check if the source IP address has already been blacklisted for the current time period
                        if i in blacklist.get(key, []):
                            continue
                        else:
                            detected = True
                            # Set the reason for blacklisting the source IP address
                            reason = 'Reason: Fan-Out-Rate in the past {} seconds was {} > {}'.format(ages[i], source_connections[key][i], max_connections[i])
                            # Add the time period to the blacklist for the source IP address
                            blacklist[key] = blacklist.get(key, []) + [i]
                            break

                if detected:
                    # Print details about the blacklisted source IP address and its fan-out rates
                    print('Port Scanner Detected from IP Address: {}'.format(key))
                    fanout_per_1s = source_connections[key][2] / 300
                    fanout_per_1m = source_connections[key][1] / 5
                    fanout_per_5m = source_connections[key][0]
                    print('   Average Fan-Out Rate Per-Second Over the Last 5mins: {}'.format(fanout_per_1s))
                    print('   Average Fan-Out Rate Per-Minute Over the Last 5mins: {}'.format(fanout_per_1m))
                    print('   Average Fan-Out Rate Per-5-Minutes Over the Last 5mins: {}'.format(fanout_per_5m))
                    print(reason)
                    print('')
