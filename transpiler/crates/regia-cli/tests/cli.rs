//! Checks that the `regia` binary prints its string.

#![allow(clippy::missing_panics_doc, reason = "a panic is how a test fails")]

use std::process::Command;

/// `regia` prints its fixed line.
#[test]
fn regia_prints_its_string() {
    let output = Command::new(env!("CARGO_BIN_EXE_regia"))
        .output()
        .expect("regia should run");
    let stdout = String::from_utf8(output.stdout).expect("output should be UTF-8");
    assert_eq!(stdout, "Salta la rana, dentro lo stagno\n");
}
