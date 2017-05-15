package utils {

    import Error._

    object Error
    {
        object Domain extends Enumeration
        {
            val Global = Value
        }
        type Domain = Domain.Value

        object LocationType extends Enumeration
        {
            val Header, Parameter = Value
        }
        type LocationType = LocationType.Value

        object Reason extends Enumeration
        {
            val Invalid, Required = Value
        }
        type Reason = Reason.Value
    }

    case class Error(domain: Domain, reason: Reason, locationType: LocationType, location: String, message: String)

}
