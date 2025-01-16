"""
  %borrowed%: https://systemweakness.com/stress-testing-a-graphql-endpoint-with-python-script-c9852b40a084
"""

import requests
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
import random


url = "https://maps.trimet.org/otp"

headers = {
    "Content-Type": "application/json",
    "Authorization": "<token HERE>"
    # Add any additional headers as needed
}

lock = threading.Lock()
exit_flag = threading.Event()
success_counter = 0

def execute_query(query):
    global success_counter
    payload = {
        # use this payload if query is going a query
        # "query": query
        
        # simple send the query as in request.py file
        query
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with lock:
            success_counter += 1
        print(f"{Fore.GREEN}GraphQL query executed successfully:{Style.RESET_ALL}")
        print(response.json())
    else:
        print(f"{Fore.RED}GraphQL query failed with status code: {response.status_code}{Style.RESET_ALL}")
        print(response.text)

graphql_queries = [
    # Query 1
    {
        "query": 'query Plan($arriveBy: Boolean, $banned: InputBanned, $bikeReluctance: Float, $carReluctance: Float, $date: String, $fromPlace: String\u0021, $modes: [TransportMode], $numItineraries: Int, $preferred: InputPreferred, $time: String, $toPlace: String\u0021, $unpreferred: InputUnpreferred, $walkReluctance: Float, $walkSpeed: Float, $wheelchair: Boolean) {\\n  plan(\\n    arriveBy: $arriveBy\\n    banned: $banned\\n    bikeReluctance: $bikeReluctance\\n    carReluctance: $carReluctance\\n    date: $date\\n    fromPlace: $fromPlace\\n    locale: \\"en\\"\\n    numItineraries: $numItineraries\\n    preferred: $preferred\\n    time: $time\\n    toPlace: $toPlace\\n    transportModes: $modes\\n    unpreferred: $unpreferred\\n    walkReluctance: $walkReluctance\\n    walkSpeed: $walkSpeed\\n    wheelchair: $wheelchair\\n  ) {\\n    itineraries {\\n      accessibilityScore\\n      duration\\n      endTime\\n      legs {\\n        accessibilityScore\\n        agency {\\n          alerts {\\n            alertDescriptionText\\n            alertHeaderText\\n            alertUrl\\n            effectiveStartDate\\n            id\\n          }\\n          gtfsId\\n          id: gtfsId\\n          name\\n          timezone\\n          url\\n        }\\n        alerts {\\n          alertDescriptionText\\n          alertHeaderText\\n          alertUrl\\n          effectiveStartDate\\n          id\\n        }\\n        arrivalDelay\\n        departureDelay\\n        distance\\n        dropOffBookingInfo {\\n          contactInfo {\\n            bookingUrl\\n            infoUrl\\n            phoneNumber\\n          }\\n          earliestBookingTime {\\n            daysPrior\\n            time\\n          }\\n          latestBookingTime {\\n            daysPrior\\n            time\\n          }\\n          message\\n        }\\n        dropoffType\\n        duration\\n        endTime\\n        fareProducts {\\n          id\\n          product {\\n            __typename\\n            id\\n            medium {\\n              id\\n              name\\n            }\\n            name\\n            riderCategory {\\n              id\\n              name\\n            }\\n            ... on DefaultFareProduct {\\n              price {\\n                amount\\n                currency {\\n                  code\\n                  digits\\n                }\\n              }\\n            }\\n          }\\n        }\\n        from {\\n          lat\\n          lon\\n          name\\n          rentalVehicle {\\n            id\\n            network\\n          }\\n          stop {\\n            alerts {\\n              alertDescriptionText\\n              alertHeaderText\\n              alertUrl\\n              effectiveStartDate\\n              id\\n            }\\n            code\\n            gtfsId\\n            id\\n            lat\\n            lon\\n          }\\n          vertexType\\n        }\\n        headsign\\n        interlineWithPreviousLeg\\n        intermediateStops {\\n          lat\\n          locationType\\n          lon\\n          name\\n          stopCode: code\\n          stopId: id\\n        }\\n        legGeometry {\\n          length\\n          points\\n        }\\n        mode\\n        pickupBookingInfo {\\n          contactInfo {\\n            bookingUrl\\n            infoUrl\\n            phoneNumber\\n          }\\n          earliestBookingTime {\\n            daysPrior\\n            time\\n          }\\n          latestBookingTime {\\n            daysPrior\\n            time\\n          }\\n          message\\n        }\\n        pickupType\\n        realTime\\n        realtimeState\\n        rentedBike\\n        rideHailingEstimate {\\n          arrival\\n          maxPrice {\\n            amount\\n            currency {\\n              code\\n            }\\n          }\\n          minPrice {\\n            amount\\n            currency {\\n              code\\n            }\\n          }\\n          provider {\\n            id\\n          }\\n        }\\n        route {\\n          alerts {\\n            alertDescriptionText\\n            alertHeaderText\\n            alertUrl\\n            effectiveStartDate\\n            id\\n          }\\n          color\\n          gtfsId\\n          id: gtfsId\\n          longName\\n          shortName\\n          textColor\\n          type\\n        }\\n        startTime\\n        steps {\\n          absoluteDirection\\n          alerts {\\n            alertDescriptionText\\n            alertHeaderText\\n            alertUrl\\n            effectiveStartDate\\n            id\\n          }\\n          area\\n          distance\\n          elevationProfile {\\n            distance\\n            elevation\\n          }\\n          lat\\n          lon\\n          relativeDirection\\n          stayOn\\n          streetName\\n        }\\n        to {\\n          lat\\n          lon\\n          name\\n          rentalVehicle {\\n            id\\n            network\\n          }\\n          stop {\\n            alerts {\\n              alertDescriptionText\\n              alertHeaderText\\n              alertUrl\\n              effectiveStartDate\\n              id\\n            }\\n            code\\n            gtfsId\\n            id\\n            lat\\n            lon\\n          }\\n          vertexType\\n        }\\n        transitLeg\\n        trip {\\n          arrivalStoptime {\\n            stop {\\n              gtfsId\\n              id\\n            }\\n            stopPosition\\n          }\\n          departureStoptime {\\n            stop {\\n              gtfsId\\n              id\\n            }\\n            stopPosition\\n          }\\n          gtfsId\\n          id\\n        }\\n      }\\n      startTime\\n      transfers: numberOfTransfers\\n      waitingTime\\n      walkTime\\n    }\\n    routingErrors {\\n      code\\n      description\\n      inputField\\n    }\\n  }\\n}","variables":{"arriveBy":false,"banned":{},"date":"${d}","fromPlace":"PDX, Portland::45.589178,-122.593464","modes":[{"mode":"BICYCLE"}],"numItineraries":3,"time":"${t}","toPlace":"Oregon Zoo, Portland::45.510074,-122.715966","walkReluctance":5}}'
    }
 ]

def run_query():
    while not exit_flag.is_set():
        with lock:
            query = random.choice(graphql_queries)
        execute_query(query)


def main():
    print(f"{Fore.CYAN}Threaded GraphQL Load Testing Script{Style.RESET_ALL}")

    # Prompt the user for the number of threads
    num_threads = int(input("Enter the number of threads to use: "))

    # Create and start the worker threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=run_query)
        thread.start()
        threads.append(thread)

    try:
        # Keep the main thread alive until interrupted
        while True:
            pass
    except KeyboardInterrupt:
        print("Interrupt signal received. Stopping the load testing...")
        exit_flag.set()
        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print(f"{Fore.GREEN}Successful requests: {success_counter}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
