
<%namespace name="d" file="/template.defs"/>
{
  planConnection(
    ${d.plan_connection_od_params()}
    modes: {
      directOnly: false
      transitOnly: false
      direct: [WALK]
      transit: {
        access: [BICYCLE_RENTAL, WALK]
        transfer: [WALK]
        egress: [BICYCLE_RENTAL, WALK]
        transit: [{ mode: TRAM, cost: { reluctance: 1.3 } }, { mode: BUS }]
      }
    }
    preferences: {
      accessibility: { wheelchair: { enabled: true } }
      street: {
        bicycle: {
          reluctance: 3.0
          speed: 7.4
          optimization: { type: SAFEST_STREETS }
          boardCost: 200
          walk: {
            speed: 1.3
            cost: { mountDismountCost: 100, reluctance: 3.5 }
            mountDismountTime: "PT5S"
          }
          rental: {
            destinationBicyclePolicy: { allowKeeping: true, keepingCost: 300 }
            allowedNetworks: ["foo", "bar"]
            bannedNetworks: ["foobar"]
          }
          parking: {
            unpreferredCost: 200
            preferred: [{ select: [{ tags: ["best-park"] }] }]
            filters: [{ not: [{ tags: ["worst-park"] }] }]
          }
        }
        walk: { speed: 2.4, reluctance: 1.5, safetyFactor: 0.5, boardCost: 200 }
      }
      transit: {
        board: { waitReluctance: 3.2, slack: "PT1M30S" }
        alight: { slack: "PT0S" }
        transfer: {
          cost: 200
          slack: "PT2M"
          maximumAdditionalTransfers: 2
          maximumTransfers: 5
        }
        timetable: {
          excludeRealTimeUpdates: false
          includePlannedCancellations: false
          includeRealTimeCancellations: true
        }
      }
    }
    locale: "en"
  ) {
    searchDateTime
    routingErrors {
      code
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
      searchWindowUsed
    }
    edges {
      cursor
      node {
        start
        end
        # next two are deprecated
        startTime
        endTime
        generalizedCost
        accessibilityScore
        emissionsPerPerson {
          co2
        }
        numberOfTransfers
        walkDistance
        walkTime
        legs {
          mode
          start {
            scheduledTime
            estimated {
              time
              delay
            }
          }
          end {
            scheduledTime
            estimated {
              time
              delay
            }
          }
          from {
            name
            lat
            lon
            arrival {
              scheduledTime
              estimated {
                delay
                time
              }
            }
            departure {
              scheduledTime
              estimated {
                delay
                time
              }
            }
            departureTime
            arrivalTime
          }
          to {
            name
            lat
            lon
            arrival {
              scheduledTime
              estimated {
                delay
                time
              }
            }
            departure {
              scheduledTime
              estimated {
                delay
                time
              }
            }
            departureTime
            arrivalTime
          }
          startTime
          endTime
          mode
          generalizedCost
          headsign
          trip {
            tripHeadsign
          }
          intermediatePlaces {
            arrival {
              scheduledTime
              estimated {
                time
                delay
              }
            }
            departure {
              scheduledTime
              estimated {
                time
                delay
              }
            }
            stop {
              name
            }
          }
          alerts {
            id
            alertHeaderText
            alertDescriptionText
            alertEffect
            alertCause
            alertSeverityLevel
            alertUrl
            effectiveStartDate
            effectiveEndDate
            entities {
              ... on Stop {
                name
                gtfsId
                lat
                lon
              }
            }
          }
          rideHailingEstimate {
            provider {
              id
            }
            productName
            minPrice {
              currency {
                code
                digits
              }
              amount
            }
            maxPrice {
              currency {
                code
                digits
              }
              amount
            }
            arrival
          }
          accessibilityScore
          id
          realtimeState
        }
      }
    }
  }
}
