{
    plan(
        from: { lat: 45.5552, lon: -122.6534 }
        to: { lat: 45.4908, lon: -122.5519 }
        date: "2025-02-15",
        time: "11:37",
        %if modes:
        transportModes: [
            {
                mode: WALK
            },
            {
                mode: TRANSIT
            },
        ]
        %endif
        ) {
        itineraries {
            startTime
            endTime
            legs {
                mode
                startTime
                endTime
                from {
                    name
                    lat
                    lon
                    departureTime
                    arrivalTime
                }
                to {
                    name
                    lat
                    lon
                    departureTime
                    arrivalTime
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
