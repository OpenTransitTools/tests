{
  planConnection(
    origin: {
      location: { coordinate: { latitude: 45.5552, longitude: -122.6534 } }
    }
    destination: {
      location: { coordinate: { latitude: 45.4908, longitude: -122.5519 } }
    }
    dateTime: { earliestDeparture: "2023-02-02T14:30-07:00" }
    modes: {
      direct: [WALK]
      transit: { transit: [{ mode: BUS }, { mode: RAIL }] }
    }
  ) {
    edges {
      node {
        start
        end
        legs {
          mode
          from {
            name
            lat
            lon
            departure {
              scheduledTime
              estimated {
                time
                delay
              }
            }
          }
          to {
            name
            lat
            lon
            arrival {
              scheduledTime
              estimated {
                time
                delay
              }
            }
          }
          route {
            gtfsId
            longName
            shortName
          }
          legGeometry {
            points
          }
        }
      }
    }
  }
}
