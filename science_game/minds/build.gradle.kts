plugins {
    java
}

defaultTasks("run")

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    maven { url = uri("https://raw.githubusercontent.com/jacamo-lang/mvn-repo/master") }
    maven { url = uri("https://repo.gradle.org/gradle/libs-releases") }
    mavenCentral()
}

dependencies {
    implementation("org.jacamo:jacamo:1.2")
    implementation("org.java-websocket:Java-WebSocket:1.5.6")
    implementation("org.json:json:20230227")
}

sourceSets {
    main {
        java {
            srcDir("src/")
        }
    }
}

tasks.register<JavaExec>("run") {
    description = "runs the application"
    group = "JaCaMo"
    dependsOn("classes")
    mainClass = "jacamo.infra.JaCaMoLauncher"
    args("science.jcm")
    classpath = sourceSets.main.get().runtimeClasspath
    javaLauncher = javaToolchains.launcherFor(java.toolchain)

    // logging.properties writes to logs/, which a fresh clone lacks
    doFirst { file("logs").mkdirs() }

    // Set logging to console
    standardOutput = System.out
    errorOutput = System.err

    // Direct Java Util Logging to Console
    systemProperty("java.util.logging.config.class", "java.util.logging.SimpleFormatter")
}
