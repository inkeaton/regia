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

// The agents in src/agt/gen/ are never tracked: every build regenerates them
// from src/regia/ when a .regia file or the transpiler has changed.
val compileRegia = tasks.register<Exec>("compileRegia") {
    description = "compiles the Regia sources to AgentSpeak"
    group = "JaCaMo"

    val repoRoot = file("../..")
    val genDir = file("src/agt/gen")

    inputs.dir("src/regia")
    inputs.files(fileTree("$repoRoot/language/src/regia") { include("**/*.py", "**/*.lark") })
        .ignoreEmptyDirectories()  // __pycache__
    inputs.files("$repoRoot/language/pyproject.toml", "$repoRoot/uv.lock", "$repoRoot/.python-version")
    outputs.dir(genDir)

    commandLine(
        "uv", "run", "--project", repoRoot.path, "--package", "regia", "--locked",
        "regia", "compile", "src/regia/for_science.regia", "-o", genDir.path,
    )

    doFirst {
        val uv = System.getenv("PATH").orEmpty().split(File.pathSeparator)
            .flatMap { listOf(File(it, "uv"), File(it, "uv.exe")) }
            .firstOrNull { it.isFile && it.canExecute() }
            ?: throw GradleException(
                "uv was not found on the PATH. It runs the Regia transpiler that generates the agents. " +
                    "Install it from https://docs.astral.sh/uv/ and try again."
            )
        executable = uv.path

        // The compiler doesn't remove agents whose source is gone
        delete(genDir)
    }
}

// compileJava comes before classes and run, and its source tree contains genDir
tasks.compileJava { dependsOn(compileRegia) }

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
