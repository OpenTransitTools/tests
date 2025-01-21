<%namespace name="d" file="/template.defs"/>
{
    ${d.plan_connection_od_params()}
    modes: {
      direct: [WALK]
      transit: { transit: [{ mode: BUS }, { mode: RAIL }] }
    }
  ) {
    edges {
      node {
        legs {
          mode
          from {
            name
            lat
            lon
          }
          to {
            name
            lat
            lon
          }
          mode
          generalizedCost
          fareProducts {
            id
            product {
              id
              name
              __typename
              ... on DefaultFareProduct {
                price {
                  currency {
                    digits
                    code
                  }
                  amount
                }
              }
              riderCategory {
                id
                name
              }
              medium {
                id
                name
              }
            }
          }
        }
      }
    }
  }
}
