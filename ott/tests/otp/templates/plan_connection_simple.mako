{
  planConnection(
    origin: {
      %if flat and flon:
      location: { coordinate: { latitude: ${flat}, longitude: ${flon} } }
      %else:
      location: { coordinate: { latitude: 45.5552, longitude: -122.6534 } }
      %endif
    }
    destination: {
      %if tlat and tlon:
      location: { coordinate: { latitude: ${tlat}, longitude: ${tlon} } }
      %else:
      location: { coordinate: { latitude: 45.4908, longitude: -122.5519 } }
      %endif
    }
    %if tripDateTime:
    dateTime: { earliestDeparture: ${tripDateTime} }
    %endif
    %if numResults:
    first: ${numResults}
    %else:
    first: 6
    %endif
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
          %if not skip_geom:
          legGeometry {
            points
          }
          %endif
        }
      }
    }
  }
}
