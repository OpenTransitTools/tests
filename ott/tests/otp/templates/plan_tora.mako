{
    plan (
        date: "",
        time: "14:21",
        fromPlace: "${fromPlace}",
        toPlace: "${toPlace}",
        arriveBy: false,
        searchWindow: 4800,
        transportModes: [{ mode: WALK}, {mode: BUS}],
        banned: {},
        locale: "en",
        walkReluctance: 4,
        walkSpeed: 1.34,
        allowedVehicleRentalNetworks: "",
        bikeReluctance: 1.0,
        bikeSpeed: 2.5,
        carReluctance: 1.0
    ) {
        itineraries {
            accessibilityScore
            walkTime
            walkDistance
            duration
            endTime
            legs {
                accessibilityScore
                agency {
                    alerts {
                        alertDescriptionText
                        alertHeaderText
                        alertUrl
                        effectiveStartDate
                        id
                    }
                    fareUrl
                    gtfsId
                    id: gtfsId
                    name
                    timezone
                    url
                }
                alerts {
                    alertDescriptionText
                    alertHeaderText
                    alertUrl
                    effectiveStartDate
                    id
                }
                arrivalDelay
                departureDelay
                distance
                dropOffBookingInfo {
                    contactInfo {
                        bookingUrl
                        infoUrl
                        phoneNumber
                    }
                    earliestBookingTime {
                        daysPrior
                        time
                    }
                    latestBookingTime {
                        daysPrior
                        time
                    }
                    message
                }
                dropoffType
                duration
                endTime
                fareProducts {
                    id
                    product {
                        __typename
                        id
                        medium {
                            id
                            name
                        }
                        name
                        riderCategory {
                            id
                            name
                        }
                        ... on DefaultFareProduct {
                            price {
                                amount
                                currency {
                                    code
                                    digits
                                }
                            }
                        }
                    }
                }
                from {
                    lat
                    lon
                    name
                    vehicleRentalStation {
                        name
                        rentalNetwork {
                            networkId
                        }
                    }
                    rentalVehicle {
                        id
                        network
                    }
                    stop {
                        alerts {
                            alertDescriptionText
                            alertHeaderText
                            alertUrl
                            effectiveStartDate
                            id
                        }
                        code
                        gtfsId
                        id
                        lat
                        lon
                    }
                    vertexType
                }
                headsign
                interlineWithPreviousLeg
                intermediateStops {
                    lat
                    locationType
                    lon
                    name
                    stopCode: code
                    stopId: id
                }
                legGeometry {
                    length
                    points
                }
                mode
                pickupBookingInfo {
                    contactInfo {
                        bookingUrl
                        infoUrl
                        phoneNumber
                    }
                    earliestBookingTime {
                        daysPrior
                        time
                    }
                    latestBookingTime {
                        daysPrior
                        time
                    }
                    message
                }
                pickupType
                realTime
                realtimeState
                rentedBike
                rideHailingEstimate {
                    arrival
                    maxPrice {
                        amount
                        currency {
                            code
                        }
                    }
                    minPrice {
                        amount
                        currency {
                            code
                        }
                    }
                    provider {
                        id
                    }
                }
                route {
                    alerts {
                        alertDescriptionText
                        alertHeaderText
                        alertUrl
                        effectiveStartDate
                        id
                    }
                    color
                    gtfsId
                    id: gtfsId
                    longName
                    shortName
                    textColor
                    type
                }
                startTime
                steps {
                    absoluteDirection
                    alerts {
                        alertDescriptionText
                        alertHeaderText
                        alertUrl
                        effectiveStartDate
                        id
                    }
                    area
                    distance
                    elevationProfile {
                        distance
                        elevation
                    }
                    lat
                    lon
                    relativeDirection
                    stayOn
                    streetName
                }
                to {
                    lat
                    lon
                    name
                    vehicleRentalStation {
                        name
                        rentalNetwork {
                            networkId
                        }
                    }
                    rentalVehicle {
                        id
                        network
                    }
                    stop {
                        alerts {
                            alertDescriptionText
                            alertHeaderText
                            alertUrl
                            effectiveStartDate
                            id
                        }
                        code
                        gtfsId
                        id
                        lat
                        lon
                    }
                    vertexType
                }
                transitLeg
                trip {
                    arrivalStoptime {
                        stop {
                            gtfsId
                            id
                        }
                        stopPosition
                    }
                    departureStoptime {
                        stop {
                            gtfsId
                            id
                        }
                        stopPosition
                    }
                    gtfsId
                    id
                }
            }
            startTime
            transfers: numberOfTransfers
            waitingTime
            walkTime
        }
        routingErrors {
            code
            description
            inputField
        }
    }
}
