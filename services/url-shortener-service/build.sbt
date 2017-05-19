name := "url-shortener-service"
version := "0.0.1"
scalaVersion := "2.11.11"

val modules = file("modules")

aggregateProjects(
    RootProject(modules / "service-library"),
    RootProject(modules / "service-manager"),
    RootProject(modules / "url-shortener")
)
