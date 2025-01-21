<%namespace name="d" file="/template.defs"/>
{
    plan(
        ${d.plan_od_params()}
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
