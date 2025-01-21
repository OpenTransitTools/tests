{
    plan(
        %if tlat and tlon:
        from: { lat: ${flat}, lon: ${flon} }
        %else:
        from: { lat: 45.5552, lon: -122.6534 }
        %endif
        %if tlat and tlon:
        to: { lat: ${tlat}, lon: ${tlon} }
        %else:
        to: { lat: 45.4908, lon: -122.5519 }
        %endif
        %if date:
        date: "${date}",
        %endif
        %if time:
        time: "${time}",
        %endif
        %if modes:
        transportModes: ${modes}
        %else:
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
                %if not skip_geom:
                legGeometry {
                    points
                }
                %endif
            }
        }
    }
}
