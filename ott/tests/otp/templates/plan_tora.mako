<%namespace name="utils" file="/template.defs"/>
{
    plan (
        date: "${date}",
        time: "${time}",
        fromPlace: "${fromPlace}",
        toPlace: "${toPlace}",
        arriveBy: ${str(arriveBy).lower()},
        searchWindow: ${searchWindow},
        transportModes: [${utils.get_modes(transportModes)}],
        allowedVehicleRentalNetworks: "${allowedVehicleRentalNetworks}",
        %if banned:
        banned: {agencies: "${banned}"},
        %endif
        locale: "${locale}",
        walkReluctance: ${walkReluctance},
        walkSpeed: ${walkSpeed},
        bikeReluctance: ${bikeReluctance},
        bikeSpeed: ${bikeSpeed},
        carReluctance: ${carReluctance}
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
