<%namespace name="d" file="/template.defs"/>
{
  planConnection(
    ${d.plan_connection_od_params()}
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
